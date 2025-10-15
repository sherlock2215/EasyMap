import os
import cdsapi
import datetime
from map import create_water_stations_from_json, enhance_water_stations_with_forecast

# ===============================
# CONFIGURATION
# ===============================
BASE_PATH = r"C:\Users\gosia\Downloads\EasyMap2\EasyMap"
FORECAST_FILE = os.path.join(BASE_PATH, "forecast.grib")
STATIONS_JSON = os.path.join(BASE_PATH, "stations.json")
OUTPUT_GEOJSON = os.path.join(BASE_PATH, "germany_waterlevels_with_forecast.geojson")
RAW_STATIONS_GEOJSON = os.path.join(BASE_PATH, "germany_waterlevels.geojson")

# Geographic bounding box for Germany region (approx)
AREA = [52.7, 12.0, 52.3, 13.8]  # [North, West, South, East]


# ===============================
# STEP 1: Download GloFAS Forecast
# ===============================
def download_forecast():
    """Download the latest GloFAS river discharge forecast from Copernicus."""
    print("📡 Downloading latest GloFAS forecast...")

    today = datetime.date.today()
    dataset = "cems-glofas-forecast"
    request = {
        "system_version": "operational",
        "hydrological_model": "lisflood",
        "product_type": "control_forecast",
        "variable": "river_discharge_in_the_last_24_hours",
        "year": str(today.year),
        "month": f"{today.month:02d}",
        "day": f"{today.day:02d}",
        "leadtime_hour": ["24", "48", "72"],
        "data_format": "grib",
        "area": AREA
    }

    client = cdsapi.Client()
    client.retrieve(dataset, request, FORECAST_FILE)

    print(f"✅ Forecast saved to: {FORECAST_FILE}")
    return FORECAST_FILE


# ===============================
# STEP 2: Process Data & Enhance Map
# ===============================
def process_forecast():
    print("\n🚀 Starting flood risk analysis...")

    # Create water stations GeoJSON
    water_stations_file = create_water_stations_from_json(
        STATIONS_JSON,
        RAW_STATIONS_GEOJSON
    )

    # Enhance with discharge forecasts
    enhanced_stations = enhance_water_stations_with_forecast(
        water_stations_file=water_stations_file,
        discharge_grib_file=FORECAST_FILE,
        output_file=OUTPUT_GEOJSON,
        debug=True
    )

    print("\n🎉 ENHANCED FLOOD ANALYSIS COMPLETE!")
    print(f"📁 Output file: {OUTPUT_GEOJSON}")
    print(f"📍 Enhanced stations: {len(enhanced_stations)}")

    # Show sample data
    print("\n🔍 SAMPLE STATIONS:")
    sample = enhanced_stations.head(5)[['station', 'avg_discharge', 'flood_risk_category']]
    for _, row in sample.iterrows():
        print(f"   {row['station']}: Discharge={row['avg_discharge']:.1f}, Risk={row['flood_risk_category']}")


# ===============================
# MAIN PIPELINE
# ===============================
if __name__ == "__main__":
    print("🌊 EasyMap Automation Started")
    try:
        forecast_path = download_forecast()
        process_forecast()
        print("\n✅ All tasks complete. Flood map successfully updated.")
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
