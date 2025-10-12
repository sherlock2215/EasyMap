import xarray as xr
import geopandas as gpd
import json
import os
from shapely.geometry import Point
import numpy as np


def enhance_water_stations_with_forecast(water_stations_file, discharge_grib_file, output_file, debug=False):
    """
    Enhance existing water stations GeoJSON with river discharge forecasts
    """
    print("1️⃣  Loading water stations...")
    water_stations = gpd.read_file(water_stations_file)
    print(f"   Found {len(water_stations)} water stations")

    print("2️⃣  Loading discharge forecast...")
    ds = xr.open_dataset(discharge_grib_file, engine="cfgrib")
    discharge_data = ds["dis24"]
    num_steps = len(discharge_data.step.values)
    print(f"   Forecast steps: {list(discharge_data.step.values)}")
    print(f"   Number of steps: {num_steps}")

    # Check units and apply scaling if necessary
    units = discharge_data.attrs.get("units", "").lower()
    print(f"   Discharge units: {units}")
    scale_factor = 1.0

    if "kg" in units or "mm" in units or "m**2" in units:
        print("⚠️  Detected per-area discharge — applying scaling factor ×1000 (approximate correction).")
        scale_factor = 1000.0

    print("3️⃣  Enhancing stations with forecast data...")
    enhanced_features = []
    stations_with_data = 0

    for idx, station in water_stations.iterrows():
        station_point = station.geometry
        station_props = station.copy()

        try:
            nearest_discharge = discharge_data.sel(
                longitude=station_point.x,
                latitude=station_point.y,
                method="nearest"
            )

            # Add forecast values for each step
            forecast_data = {}
            discharge_values = []

            for i, step in enumerate(discharge_data.step.values):
                step_discharge = float(nearest_discharge.sel(step=step)) * scale_factor
                if np.isnan(step_discharge):
                    step_discharge = 0.0
                forecast_data[f'discharge_step_{i + 1}'] = step_discharge
                forecast_data[f'discharge_{i + 1}day'] = step_discharge
                discharge_values.append(step_discharge)

            if debug and idx < 5:
                print(f"   {station_props.get('station', 'unknown')} → {discharge_values}")

            # Skip stations that have all 0 or NaN values
            if all(v == 0 or np.isnan(v) for v in discharge_values):
                station_props['flood_risk_category'] = 'Unknown'
                station_props['avg_discharge'] = 0
                station_props['forecast_steps'] = 0
                enhanced_features.append(station_props)
                continue

            avg_discharge = np.mean(discharge_values)
            risk_score = calculate_flood_risk(avg_discharge, forecast_data, num_steps)
            station_props.update(forecast_data)
            station_props['avg_discharge'] = avg_discharge
            station_props['flood_risk_score'] = risk_score
            station_props['flood_risk_category'] = categorize_risk(risk_score)
            station_props['forecast_steps'] = num_steps
            stations_with_data += 1

        except Exception as e:
            print(f"   ⚠️  Could not process station {station_props.get('station', 'unknown')}: {e}")
            station_props['flood_risk_category'] = 'Unknown'
            station_props['forecast_steps'] = 0

        enhanced_features.append(station_props)

    print(f"   Successfully enhanced {stations_with_data} stations with forecast data")

    print("4️⃣  Creating enhanced GeoJSON...")
    enhanced_gdf = gpd.GeoDataFrame(enhanced_features, crs=water_stations.crs)

    print("5️⃣  Saving results...")
    enhanced_gdf.to_file(output_file, driver='GeoJSON')

    # Print summary
    print("\n📊 FLOOD RISK SUMMARY:")
    risk_counts = enhanced_gdf['flood_risk_category'].value_counts()
    for category, count in risk_counts.items():
        print(f"   {category}: {count} stations")

    if 'avg_discharge' in enhanced_gdf.columns:
        avg_discharge = enhanced_gdf['avg_discharge'].mean()
        print(f"   Average discharge: {avg_discharge:.2f} (scaled units)")

    return enhanced_gdf


def calculate_flood_risk(avg_discharge, forecast_data, num_steps):
    risk_score = 0

    # Calibrated thresholds (more sensitive)
    if avg_discharge > 400:
        risk_score += 4
    elif avg_discharge > 250:
        risk_score += 3
    elif avg_discharge > 150:
        risk_score += 2
    elif avg_discharge > 50:
        risk_score += 1

    # Trend factor
    if num_steps >= 2:
        values = [forecast_data[f'discharge_step_{i+1}'] for i in range(num_steps)]
        if values[0] != 0:
            trend = (values[-1] - values[0]) / abs(values[0])
            if trend > 0.3:
                risk_score += 3
            elif trend > 0.15:
                risk_score += 2
            elif trend > 0.05:
                risk_score += 1

    return risk_score


def categorize_risk(score):
    """Categorize flood risk based on score"""
    if score >= 6:
        return "Extreme"
    elif score >= 5:
        return "High"
    elif score >= 3:
        return "Medium"
    elif score >= 1:
        return "Low"
    else:
        return "Very Low"


def create_water_stations_from_json(json_file, output_geojson):
    """
    Create initial water stations GeoJSON from your JSON data
    """
    print("🌊 Creating water stations GeoJSON from JSON data...")

    with open(json_file, encoding="utf-8") as f:
        data = json.load(f)

    geojson = {
        "type": "FeatureCollection",
        "features": []
    }

    stations_created = 0
    for s in data:
        if s.get("longitude") and s.get("latitude"):
            geojson["features"].append({
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [s["longitude"], s["latitude"]]
                },
                "properties": {
                    "station": s.get("shortname"),
                    "river_km": s.get("km"),
                    "agency": s.get("agency"),
                    "station_id": s.get("number"),
                    "river_name": s.get("water", {}).get("shortname")
                }
            })
            stations_created += 1

    with open(output_geojson, "w") as f:
        json.dump(geojson, f, indent=2)

    print(f"✅ Created {stations_created} water stations in {output_geojson}")
    return output_geojson


if __name__ == "__main__":
    base_path = "C:/Users/gosia/Downloads/EasyMap2/EasyMap"

    print("🚀 Starting flood risk analysis...")

    # Step 1: Create water stations GeoJSON
    water_stations_file = create_water_stations_from_json(
        os.path.join(base_path, "stations.json"),
        os.path.join(base_path, "germany_waterlevels.geojson")
    )

    # Step 2: Enhance with discharge forecasts
    enhanced_stations = enhance_water_stations_with_forecast(
        water_stations_file=water_stations_file,
        discharge_grib_file=os.path.join(base_path, "forecast.grib"),
        output_file=os.path.join(base_path, "germany_waterlevels_with_forecast.geojson"),
        debug=True  # 👈 Set to True to print first few stations' discharge values
    )

    print("\n🎉 ENHANCED FLOOD ANALYSIS COMPLETE!")
    print(f"📁 Output file: {os.path.join(base_path, 'germany_waterlevels_with_forecast.geojson')}")
    print(f"📍 Enhanced stations: {len(enhanced_stations)}")

    print("\n🔍 SAMPLE STATIONS:")
    sample = enhanced_stations.head(5)[['station', 'avg_discharge', 'flood_risk_category']]
    for _, row in sample.iterrows():
        print(f"   {row['station']}: Discharge={row['avg_discharge']:.1f}, Risk={row['flood_risk_category']}")
