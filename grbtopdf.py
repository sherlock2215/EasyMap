import xarray as xr
import rioxarray

# Try opening with different parameters
try:
    # Method 1: Basic open
    ds = xr.open_dataset("forecast.grib", engine="cfgrib")
    print("✅ Opened with basic parameters")
except Exception as e:
    print(f"❌ Basic open failed: {e}")
    try:
        # Method 2: Try different backend options
        ds = xr.open_dataset("forecast.grib", engine="cfgrib", backend_kwargs={'filter_by_keys': {'typeOfLevel': 'surface'}})
        print("✅ Opened with filter_by_keys")
    except Exception as e:
        print(f"❌ Second attempt failed: {e}")
        # Method 3: List available variables first
        try:
            datasets = xr.open_dataset("forecast.grib", engine="cfgrib", backend_kwargs={'errors': 'ignore'})
            print("Available variables:", list(datasets.data_vars))
            ds = datasets
        except Exception as e:
            print(f"❌ All methods failed: {e}")
            exit()

# See what variables you actually have
print("Available variables:", list(ds.data_vars))
print("Available coordinates:", list(ds.coords))

# Check the structure
print("Dataset info:")
print(ds)