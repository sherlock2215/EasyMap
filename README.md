# 🌊 EasyMap — Automated Flood Forecast Visualization

EasyMap is a fully automated pipeline that downloads real-time **river discharge forecasts** from the [Copernicus GloFAS API](https://cds.climate.copernicus.eu/) and combines them with **local water station data** to generate an enhanced GeoJSON map showing **flood risk levels**.

---

## 🚀 Features

- 🔄 **Automatic Data Retrieval** — Downloads the latest GloFAS forecast daily.
- 🌍 **GeoJSON Output** — Produces ready-to-visualize maps for GIS or web apps.
- 📊 **Hydrological Forecast Integration** — Merges real discharge predictions into station-level analysis.
- 🧠 **Easy Customization** — Simple to extend to other countries or bounding boxes.
- 🕓 **Supports Automation** — Can run daily via Windows Task Scheduler or cron.

---

## 🧩 Project Structure

```
EasyMap/
│
├── main.py                        # Main automation script
├── map.py                         # Handles GeoJSON + data enhancement
├── grbtopdf.py                    # GRIB debugging / inspection tool
├── stations.json                  # Water station data (input)
├── forecast.grib                  # GloFAS forecast (downloaded automatically)
├── germany_waterlevels.geojson    # Base map
├── germany_waterlevels_with_forecast.geojson  # Enhanced output map
├── requirements.txt               # Dependencies
└── LICENSE                        # MIT license
```

---

## ⚙️ Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/sherlock2215/EasyMap.git
   cd EasyMap
   ```

2. **Create a virtual environment (optional but recommended)**
   ```bash
   python -m venv venv
   source venv/bin/activate   # on macOS/Linux
   venv\Scripts\activate    # on Windows
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install Copernicus CDS API key**
   - Create a free [Copernicus Data Store account](https://cds.climate.copernicus.eu/api-how-to).
   - Save your key to `~/.cdsapirc` (Linux/macOS) or `C:\Users\<you>\.cdsapirc` (Windows).

---

## ▶️ Usage

Run the full automated analysis:

```bash
python main.py
```

This will:
- Download the latest `forecast.grib` file.
- Combine it with your water station data.
- Generate an enhanced `germany_waterlevels_with_forecast.geojson` file.

---

## 🕒 Automating Daily Runs

### Windows (Task Scheduler)
1. Open **Task Scheduler**
2. Create a new task → *Run daily at 07:00*
3. Command:
   ```bash
   python "C:\Users\gosia\Downloads\EasyMap2\EasyMap\main.py"
   ```

### Linux/macOS (cron)
```bash
0 7 * * * /usr/bin/python3 /path/to/main.py
```

---

## 🧾 Example Output
Example GeoJSON snippet:

```json
{
  "station": "Berlin-Spree",
  "avg_discharge": 182.4,
  "flood_risk_category": "Moderate"
}
```

---

## 🪪 License
This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author
**Sherlock2215**  
🌐 GitHub: [@sherlock2215](https://github.com/sherlock2215)  
📍 Germany  
💬 Contributions and suggestions are welcome!
