import numpy as np
import xarray as xr


# Load the NetCDF file
#file_path = '/Users/gbenz/Downloads/tx10pETCCDI_mon_HadGEM3-GC31-LL_historical_r1i1p1f3_b1981-2010_v20190624_185001-201412_v2-0.nc'

def transform_longitudinal_values(param_etccdi_index, param_netcdf_file):
    # Check if the variable appears in the file path
    if param_etccdi_index not in param_netcdf_file:
        raise ValueError(f"STOP!! Before you break the climate '{param_etccdi_index}' does not appear in the file path '{param_netcdf_file}'.")
    else:
        print(f"The variable '{param_etccdi_index}' was found in the file path and the world continues to spin.")

    # Open the dataset
    ds = xr.open_dataset(f'/Users/gbenz/Documents/Climate Data/climate_extremes/{param_netcdf_file}')

    # Get latitude and longitude coordinates
    lat = ds['lat'].values
    lon = ds['lon'].values

    # Get the spatial extent (bounding box)
    lat_min, lat_max = lat.min(), lat.max()
    lon_min, lon_max = lon.min(), lon.max()

    print(f"Original Latitude range: {lat_min} to {lat_max}")
    print(f"Original Longitude range: {lon_min} to {lon_max}")

    # Adjust the longitude values from [0°, 360°] to [-180°, 180°]
    adjusted_lon = np.where(lon > 180, lon - 360, lon)

    # Update the longitude in the dataset
    ds = ds.assign_coords(lon=adjusted_lon)

    # Sort the dataset by the updated longitude values to maintain spatial continuity
    ds = ds.sortby('lon')

    # Print the new longitude range
    lon_min, lon_max = ds['lon'].min().values, ds['lon'].max().values
    print(f"Adjusted Longitude range: {lon_min} to {lon_max}")


    adjusted_netcdf_file = f'/Users/gbenz/Downloads/adjusted_{param_netcdf_file}.nc'
    ds.to_netcdf(adjusted_netcdf_file)

    print(f"Adjusted dataset saved to: {adjusted_netcdf_file}")

    return(ds)