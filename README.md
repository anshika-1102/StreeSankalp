# StreeSankalp

**StreeSankalp** is a comprehensive platform designed to provide support to victims and survivors of gender-based violence (GBV), sexual abuse, domestic abuse, child marriage, and other traumatic events. It aims to offer safe, accessible, and effective resources to individuals in need of help.

The platform integrates various features to assist survivors in accessing services, reporting incidents anonymously, and finding support through diverse services, including mental health, legal aid, and local shelters. Through technological integration, StreeSankalp ensures that the services and resources available are not only effective but also inclusive and easily accessible to those in need.

## Features
1. **Anonymous Reporting**: Users can anonymously report cases of abuse and violence through an easy-to-use form. The reports are securely stored and handled.
2. **Help Resources**: The platform offers a range of help resources including helplines, mental health support, legal assistance, and emergency services. 
3. **Map for Location-Based Services**: Integration with the OpenStreetMap API allows users to find nearby services such as shelters, legal assistance, hospitals, and NGOs.
4. **NGO Database**: A searchable list of NGOs that support survivors, with detailed contact information, locations, and the types of services offered.
5. **Community Support**: Integration with WhatsApp and Discord allows survivors to connect with others and access emotional and psychological support.
6. **AI-Powered Chatbot**: An AI-powered chatbot helps guide users through available resources, report incidents, and answer queries related to support services.
7. **24/7 Support**: The platform is designed to ensure that help is available at all times. Users can access resources, support, and emergency contacts at any hour.
8. **Webinars & Workshops**: Access to workshops, webinars, and educational material for survivors to understand their rights, available support systems, and healing strategies.

## Tech Stack
The project utilizes several web technologies and frameworks, ensuring a responsive, accessible, and user-friendly platform.

- **Frontend:**
  - HTML5, CSS3, SCSS
  - JavaScript
  - Bootstrap5 for responsive design
  - OpenStreetMap API for location-based services
  - jQuery for DOM manipulation
- **Backend:**
  - Python with Flask (for routing and server-side logic)
  - Integrated with Google Cloud Console for hosting and backend management
- **Other Tools:**
  - Dialogflow (Google AI) for chatbot integration
  - Git for version control
  - GitHub for repository management and hosting

## Installation
To set up the project on your local machine, follow the steps below:

### Prerequisites:
- Python 3.x
- Flask installed (`pip install Flask`)

### Steps:
1. **Clone the repository**:
   ```bash
   git clone https://github.com/anshika-1102/StreeSankalp.git
   cd StreeSankalp
   ```
2. **Install backend dependencies**:
   ```bash
    pip install -r requirements.txt
   ```
3. **Run the Flask application**:
  ```bash
``python app.py
  ```
4. Visit http://127.0.0.1:5000/ in your browser to view the app.

## Usage
Once the application is set up, you can interact with the platform via its web interface. Key actions include:

1. Reporting abuse through the anonymous reporting page.
2. Finding nearby services using the location map.
3. Accessing help resources and NGO listings.
4. Engaging with the AI-powered chatbot for instant support.

## Future Scope
The platform is continually evolving. Future enhancements include:

1. Mobile Application: A mobile app to make the platform more accessible, with offline features and notifications.
2. Case Reporting and Tracking: A feature for users to submit cases with detailed reports and track their case status through the platform.
3. Data Analytics: Implementing analytics to gather data on abuse trends, allowing organizations to better understand the needs and challenges faced by survivors.
4. Peer Support Groups: Extending the community support feature to include peer-to-peer support groups with group chat options.
5. Secure Document Sharing: Allow survivors to share documents securely with NGOs or support agencies.
6. Real-Time Video Consultations: Providing the option for real-time video consultations with therapists, legal professionals, and social workers.
