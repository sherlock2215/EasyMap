var map = L.map('map').setView([51.2, 10.5], 6);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  attribution: '&copy; OpenStreetMap contributors'
}).addTo(map);


fetch('germany_humidity.geojson')
  .then(res => res.json())
  .then(data => {
    L.geoJSON(data, {
      pointToLayer: function(feature, latlng) {
        return L.circleMarker(latlng, {
          radius: 6,
          fillColor: getColor(feature.properties.rel_humidity),
          color: '#000',
          weight: 1,
          fillOpacity: 0.8
        }).bindPopup(
          "Station: " + feature.properties.station_name +
          "<br>Humidity: " + feature.properties.rel_humidity + "%"
        );
      }
    }).addTo(map);
  });