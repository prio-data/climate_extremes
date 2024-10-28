import numpy as np
import xarray as xr

def give_metadata(param_ds):
    # Check if the variable appears in the file path


    # Get latitude and longitude coordinates
    lat = param_ds['lat'].values
    lon = param_ds['lon'].values

    # Get the spatial extent (bounding box)
    lat_min, lat_max = lat.min(), lat.max()
    lon_min, lon_max = lon.min(), lon.max()

    print(f"Latitude range: {lat_min} to {lat_max}")
    print(f"Longitude range: {lon_min} to {lon_max}")


    # Calculate latitude and longitude resolution (difference between adjacent points)
    lat_res = lat[1] - lat[0]
    lon_res = lon[1] - lon[0]

    print(f"Latitude resolution: {lat_res}")
    print(f"Longitude resolution: {lon_res}")

    # Get global attributes of the dataset
    global_attrs = param_ds.attrs

    # Print the global metadata
    print("Global Metadata:")
    for key, value in global_attrs.items():
        print(f"{key}: {value}")

    # Extract unique years and months using cftime attributes
    unique_years = sorted(set(param_ds['time.year'].values))
    unique_months = sorted(set(param_ds['time.month'].values))

    print("Unique Years:", unique_years)
    print("Unique Months:", unique_months)