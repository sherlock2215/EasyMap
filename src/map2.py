import cdsapi

client = cdsapi.Client()

dataset = "cems-glofas-forecast"
request = {
    "system_version": "operational",
    "hydrological_model": "lisflood",
    "product_type": "control_forecast",
    "variable": "river_discharge_in_the_last_24_hours",
    "year": "2025",
    "month": "09",
    "day": "30",
    "leadtime_hour": ["24", "48", "72"],
    "data_format": "grib",
    "area": [52.7, 12.0, 52.3, 13.8]  # [North, West, South, East]
}

target = "forecast.grib"

client.retrieve(dataset, request, target)
