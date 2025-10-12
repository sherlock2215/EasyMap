# 🌊 Germany Flood Risk Monitor

A real-time flood risk monitoring system that combines weather station data with river discharge forecasts to provide early flood warnings across Germany.

---

## 🚀 Features

- **Interactive Map:** Visualize flood risk stations across Germany with color-coded risk levels  
- **Real-time Data:** Process temperature and river discharge data for accurate flood predictions  
- **Smart Search:** Search for any German city to see local flood risks within a 20 km radius  
- **Risk Assessment:** Automated flood risk scoring based on multiple environmental factors  
- **Professional Dashboard:** Clean, modern interface with real-time statistics and filtering  
- **Responsive Design:** Optimized for desktop and tablet devices  

---

## 🛠️ Tech Stack

### Backend
- **Python 3.10+** – Data processing and analysis  
- **Pandas** – Data manipulation and cleaning  
- **GeoPandas** – Spatial data processing  
- **CDS API** – River discharge forecast data from Copernicus  
- **XArray** – GRIB file processing  

### Frontend
- **Leaflet.js** – Interactive mapping  
- **Vanilla JavaScript** – Frontend logic and interactivity  
- **HTML5 / CSS3** – Modern responsive design  
- **GeoJSON** – Spatial data format  

---

## 📁 Project Structure

```
map_hackathon/
├── data_processing/
│   ├── map.py                 # Main data processing pipeline
│   ├── stations1.csv          # Weather station data
│   ├── stations2.csv          # Additional station data
│   └── germany_waterlevels_with_forecast.geojson  # Processed output
├── frontend.html              # Main web application
├── forecast.grib              # River discharge forecast data
└── README.md
```

---

## 🔧 Installation & Setup

### Prerequisites
- Python 3.10+  
- CDS API account (for river discharge data)  
- Modern web browser  

### 1️⃣ Backend Setup

```bash
# Install Python dependencies
pip install pandas geopandas xarray cfgrib cdsapi

# Set up CDS API (requires registration)
# Add your CDS API key to ~/.cdsapirc
```

### 2️⃣ Data Processing

```bash
# Run the data processing pipeline
python map.py
```

**This will:**
1. Load and merge station CSV files  
2. Process temperature data and calculate daily averages  
3. Fetch river discharge forecasts from CDS API  
4. Calculate flood risk scores  
5. Generate GeoJSON output with enhanced data  

### 3️⃣ Frontend Deployment

```bash
# Start local server
python -m http.server 8000
```

Then open in your browser:  
👉 [http://localhost:8000/frontend.html](http://localhost:8000/frontend.html)

---

## 📊 Data Sources

### Primary Data
- **Weather Stations:** Temperature and precipitation data from German meteorological stations  
- **River Discharge:** GloFAS forecast data from Copernicus Climate Data Store  
- **Spatial Data:** GeoJSON polygons for regional analysis  

### Risk Calculation Factors
- Current Discharge Levels – Real-time river flow measurements  
- Forecast Trends – 24 h, 48 h, 72 h discharge predictions  
- Temperature Patterns – Snow melt and rainfall correlations  
- Historical Baselines – Seasonal normal ranges  

---

## 🎯 Usage Guide

### For Citizens
- **Search Your City:** Type any German city name in the search bar  
- **View Local Risks:** See flood monitoring stations within a 20 km radius  
- **Understand Risk Levels:**
  - 🔴 **High:** Immediate action recommended  
  - 🟡 **Medium:** Monitor situation closely  
  - 🟢 **Low:** Normal conditions  
  - 🔵 **Very Low:** Minimal risk  

### For Authorities
- **Regional Monitoring:** Use filters to focus on high-risk areas  
- **Station Details:** Click any station for detailed metrics and forecasts  
- **Trend Analysis:** Monitor discharge trends over 3-day forecasts  

---

## 🚨 Risk Categories

| Risk Level | Discharge Range | Action Recommended     |
|-------------|----------------|------------------------|
| **Extreme** | > 600 m³/s     | Evacuation likely      |
| **High**    | 400–600 m³/s   | Emergency prep         |
| **Medium**  | 250–400 m³/s   | Close monitoring        |
| **Low**     | 150–250 m³/s   | Normal operations       |
| **Very Low**| < 150 m³/s     | No immediate concern    |

---

## 🔄 Data Flow

```
Raw Station Data 
→ Temperature Processing 
→ Spatial Join 
→ Discharge Forecasts 
→ Risk Calculation 
→ GeoJSON Export 
→ Web Visualization 
→ User Interaction
```

---

## 🎨 Customization

### Adding New Regions
1. Add regional polygons to `regions.geojson`  
2. Update station coordinates in the processing script  
3. Adjust risk thresholds for local conditions  

### Modifying Risk Algorithm

Edit the `calculate_flood_risk()` function in `map.py`:

```python
def calculate_flood_risk(avg_discharge, forecast_data, num_steps):
    # Customize thresholds and weights here
    risk_score = 0
    # Your custom logic
    return risk_score
```

---

## 📈 Future Enhancements

- Real-time data streaming  
- Mobile app version  
- Historical flood pattern analysis  
- Automated alert system  
- Multi-language support  
- Social media integration for warnings  

---

## 🤝 Contributing

1. Fork the repository  
2. Create a feature branch:  
   ```bash
   git checkout -b feature/improvement
   ```
3. Commit your changes:  
   ```bash
   git commit -am "Add new feature"
   ```
4. Push to the branch:  
   ```bash
   git push origin feature/improvement
   ```
5. Create a Pull Request  

---

## 📄 License

This project is licensed under the **MIT License** – see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **Copernicus Climate Data Store** for river discharge data  
- **German Meteorological Service** for weather station data  
- **Leaflet.js** for mapping capabilities  
- **OpenStreetMap** for base map tiles  

---

## 🆘 Emergency Contacts

In case of actual flood emergency, contact local authorities:

- **Fire Department:** 112  
- **Technical Relief Agency (THW):** Local offices  
- **Water Management Authorities:** Regional contacts  

> ⚠️ **Disclaimer:** This system provides risk assessment based on available data.  
> Always follow official warnings from local authorities during flood events.

---

**Developed with ❤️ for public safety and environmental monitoring**
