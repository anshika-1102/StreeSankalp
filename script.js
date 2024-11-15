// Initialize the map
const map = L.map('map').setView([20, 77], 5); // Initial view over India

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  maxZoom: 19,
}).addTo(map);

// Define red and blue icons for current location and nearby services
const redIcon = new L.Icon({
  iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-red.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
  shadowSize: [41, 41]
});

const blueIcon = new L.Icon({
  iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png', // default blue icon
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
  shadowSize: [41, 41]
});

// Function to get the user's current location
navigator.geolocation.getCurrentPosition(
  position => {
    const { latitude, longitude } = position.coords;
    map.setView([latitude, longitude], 13);

    // Add a red marker for the user's current location
    L.marker([latitude, longitude], { icon: redIcon, title: "Your Location" })
      .addTo(map)
      .bindPopup("You are here")
      .openPopup();

    // Fetch and display nearby places based on the initial filter selection
    fetchNearbyPlaces(latitude, longitude, document.getElementById('service-type').value);
  },
  error => console.error("Error fetching location:", error)
);

// Function to fetch and display nearby places
function fetchNearbyPlaces(lat, lon, type) {
  // Clear any existing markers except the user's red marker
  map.eachLayer(layer => {
    if (layer instanceof L.Marker && layer.options.icon !== redIcon) map.removeLayer(layer);
  });

  // Define Overpass query for the selected type
  const query = `[out:json];
    node(around:5000, ${lat}, ${lon})[amenity=${type}];
    out;`;

  const url = `https://overpass-api.de/api/interpreter?data=${encodeURIComponent(query)}`;

  // Fetch data from Overpass API
  fetch(url)
    .then(response => response.json())
    .then(data => {
      data.elements.forEach(place => {
        // Add a blue marker for each nearby service
        const marker = L.marker([place.lat, place.lon], { icon: blueIcon, title: place.tags.name || type })
          .addTo(map)
          .bindPopup(`<strong>${place.tags.name || "Unknown"}</strong><br>${type}`);
      });
    })
    .catch(error => console.error("Error fetching data:", error));
}

// Event listener for service type filter
document.getElementById('service-type').addEventListener('change', function () {
  const selectedType = this.value;
  navigator.geolocation.getCurrentPosition(
    position => {
      const { latitude, longitude } = position.coords;
      fetchNearbyPlaces(latitude, longitude, selectedType);
    },
    error => console.error("Error fetching location:", error)
  );
});