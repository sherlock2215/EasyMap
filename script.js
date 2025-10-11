// Initialize the Leaflet map
const map = L.map('map').setView([51.1657, 10.4515], 6); // Set view to center of Germany, zoom level 6

// Add OpenStreetMap base layer
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);

// Path to the GeoJSON file your colleague is creating
const geojsonFilePath = 'demo_waterlevels.geojson'; // Ensure the filename is correct

// Function to load and display GeoJSON data
async function loadAndDisplayGeoJSON() {
    try {
        const response = await fetch(geojsonFilePath); // Fetch the GeoJSON file
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json(); // Parse the JSON data

        // Add GeoJSON data to the map
        L.geoJSON(data, {
            // Function to create a marker for each point
            pointToLayer: function (feature, latlng) {
                // You can create a custom icon here if needed
                // const customIcon = L.icon({
                //     iconUrl: 'path/to/your/icon.png',
                //     iconSize: [30, 30],
                //     iconAnchor: [15, 30]
                // });
                // return L.marker(latlng, {icon: customIcon});

                // Default marker
                return L.marker(latlng);
            },
            // Function to add popups with information
            onEachFeature: function (feature, layer) {
                if (feature.properties) {
                    let p = feature.properties;
                    let popupContent = `
                        <b>Station:</b> ${p.station || 'N/A'}<br>
                        <b>Station ID:</b> ${p.station_id || 'N/A'}<br>
                        <b>River:</b> ${p.river_name || 'N/A'}<br>
                        <b>River km:</b> ${p.river_km !== undefined ? p.river_km : 'N/A'}<br>
                        <b>Agency:</b> ${p.agency || 'N/A'}<br>
                        <b>Current Water Level:</b> ${p.water_level !== null ? p.water_level + ' cm' : 'No Data'}<br>
                        <b>Avg Discharge:</b> ${p.avg_discharge !== undefined ? p.avg_discharge + ' m³/s' : 'N/A'}<br>
                        <b>Flood Risk Category:</b> ${p.flood_risk_category || 'N/A'} (Score: ${p.flood_risk_score !== undefined ? p.flood_risk_score : 'N/A'})<br>
                        <b>Forecast Steps:</b> ${p.forecast_steps !== undefined ? p.forecast_steps : 'N/A'}
                    `;
                    layer.bindPopup(popupContent);
                }
            }
            // Function to add popups with information
            // onEachFeature: function (feature, layer) {
            //     if (feature.properties) {
            //         let popupContent = `
            //             <b>Station:</b> ${feature.properties.station || 'No Name'}<br>
            //             <b>River km:</b> ${feature.properties.river_km || 'N/A'}<br>
            //             <b>Agency:</b> ${feature.properties.agency || 'N/A'}<br>
            //             <b>Water Level:</b> ${feature.properties.water_level !== undefined ? feature.properties.water_level + ' cm' : 'No Data'}
            //         `;
            //         layer.bindPopup(popupContent);
            //     }
            // }
        }).addTo(map);

        console.log('GeoJSON data loaded and displayed.');

    } catch (error) {
        console.error('Error loading or displaying GeoJSON:', error);
        // You can add a user-friendly error message to the page here
        document.querySelector('h1').textContent = 'Error loading map data.';
    }
}

// Call the function to load data when the page is ready
loadAndDisplayGeoJSON();