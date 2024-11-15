from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os
import logging
import sqlite3
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

# Initialize Flask application and add CORS
app = Flask(__name__)
CORS(app, resources={r"/service": {"origins": "*"}})

# Configure logging
logging.basicConfig(level=logging.INFO)

# Load the environment variables from .env file
load_dotenv()

# Get the SendGrid API key and email addresses from environment variables
SENDGRID_API_KEY = os.getenv('SENDGRID_API_KEY')
EMAIL_GBV = os.getenv('EMAIL_GBV')  # Gender-Based Violence
EMAIL_DV = os.getenv('EMAIL_DV')    # Domestic Violence
EMAIL_SA = os.getenv('EMAIL_SA')    # Sexual Abuse
EMAIL_ET = os.getenv('EMAIL_ET')    # Eve Teasing

# Database setup
def init_db():
    conn = sqlite3.connect('reports.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            phone_number TEXT NOT NULL,
            incident_type TEXT NOT NULL,
            complaint_details TEXT NOT NULL,
            reviewed BOOLEAN NOT NULL DEFAULT 0  -- Checkbox for reviewed status
        )
    ''')
    conn.commit()
    conn.close()

# Initialize the database
init_db()

# Function to save report to the database
def save_report_to_db(phone_number, incident_type, complaint_details):
    conn = sqlite3.connect('reports.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO reports (phone_number, incident_type, complaint_details)
        VALUES (?, ?, ?)
    ''', (phone_number, incident_type, complaint_details))
    conn.commit()
    conn.close()

# Function to get all reports from the database
def get_all_reports():
    conn = sqlite3.connect('reports.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM reports')
    rows = cursor.fetchall()
    conn.close()
    return rows

# Route to report an incident
@app.route('/service', methods=['POST'])
def report_case():
    app.logger.info('Report request received')
    phone_number = request.form.get('phone_number')
    incident_type = request.form.get('incident_type')
    complaint_details = request.form.get('complaint')

    app.logger.info(f'Received data - Phone Number: {phone_number}, Incident Type: {incident_type}, Complaint: {complaint_details}')

    if not phone_number or not incident_type or not complaint_details:
        app.logger.error('Phone number, incident type, or complaint details not provided')
        return jsonify({"success": False, "error": "All fields are required"}), 400

    # Determine the recipient based on the incident type
    recipient_email = {
        "Gender-Based Violence": EMAIL_GBV,
        "Domestic Violence": EMAIL_DV,
        "Sexual Abuse": EMAIL_SA,
        "Eve Teasing": EMAIL_ET
    }.get(incident_type)

    if not recipient_email:
        app.logger.error('Invalid incident type provided')
        return jsonify({"success": False, "error": "Invalid incident type"}), 400

    # Save the report data to the database
    save_report_to_db(phone_number, incident_type, complaint_details)

    try:
        # Create and send the email using SendGrid
        message = Mail(
            from_email='ratnaanamika0610@gmail.com',  # Replace with your verified sender email
            to_emails=recipient_email,
            subject=f"New Incident Report from {phone_number}",
            plain_text_content=f"Incident Type: {incident_type}\nPhone Number: {phone_number}\nComplaint Details:\n{complaint_details}"
        )

        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)

        app.logger.info('Email sent successfully')
        return jsonify({"success": True}), 200

    except Exception as e:
        app.logger.error(f'Error sending email: {str(e)}')
        return jsonify({"success": False, "error": str(e)}), 500

# Route to get all reports
@app.route('/reports', methods=['GET'])
def view_reports():
    reports = get_all_reports()
    report_list = [
        {
            "id": row[0],
            "phone_number": row[1],
            "incident_type": row[2],
            "complaint_details": row[3],
            "reviewed": bool(row[4])
        }
        for row in reports
    ]
    return jsonify(report_list)

# Route to update the 'reviewed' status
@app.route('/update_reviewed/<int:report_id>', methods=['PATCH'])
def update_reviewed(report_id):
    try:
        conn = sqlite3.connect('reports.db')
        cursor = conn.cursor()
        
        # Toggle the 'reviewed' status
        cursor.execute('UPDATE reports SET reviewed = NOT reviewed WHERE id = ?', (report_id,))
        conn.commit()
        
        # Check if update was successful
        if cursor.rowcount == 0:
            return jsonify({"success": False, "error": "Report not found"}), 404
        
        conn.close()
        return jsonify({"success": True}), 200
    except Exception as e:
        app.logger.error(f'Error updating reviewed status: {str(e)}')
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/')
def home():
    return jsonify({"message": "Server is running!"})

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
