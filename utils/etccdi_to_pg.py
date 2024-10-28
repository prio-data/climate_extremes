import rioxarray
import rasterio
from rasterio.enums import Resampling
import matplotlib.pyplot as plt
import os
import geopandas as gpd
from rasterstats import zonal_stats
import pandas as pd

def generate_etccdi_temporal_tables(param_time_index_list, param_netcdf, param_climate_index, param_shapefile_path):
    # Initialize an empty list to store DataFrames for each loop iteration
    all_stats = []
    
    # Retrieve the first and last time indices for file naming
    first_time_index = param_time_index_list[0]
    last_time_index = param_time_index_list[-1]
    
    # Loop through each time index
    for i in param_time_index_list:
        print(i)
        
        time_index = i
        raster_data = param_netcdf[param_climate_index].isel(time=time_index)  # Adjust time index as necessary
        date_time = str(param_netcdf['time'].isel(time=time_index).values.item())  # Converts to a scalar value
        year = date_time.split('-')[0]
        month = date_time.split('-')[1]

        # Print the raster data and year for debug
        print("Year:", date_time)

        raster_data = raster_data.rio.set_spatial_dims(x_dim='lon', y_dim='lat')

        # Set CRS if not already defined
        if not raster_data.rio.crs:
            raster_data = raster_data.rio.write_crs("EPSG:4326")  # WGS 84 Geographic Coordinate System

        # Save the raster to GeoTIFF
        raster_file_path = 'working_etccdi_file.tif'
        raster_data.rio.to_raster(raster_file_path)
        print(f"GeoTIFF saved at: {raster_file_path}")

        # Resample Raster
        raster_data = rioxarray.open_rasterio('working_etccdi_file.tif')
        raster_data = raster_data.rio.set_spatial_dims(x_dim='x', y_dim='y')
        current_resolution_x = abs(raster_data.x[1] - raster_data.x[0])
        current_resolution_y = abs(raster_data.y[1] - raster_data.y[0])
        new_resolution_x = current_resolution_x / 10
        new_resolution_y = current_resolution_y / 10
        resampled_raster = raster_data.rio.reproject(
            raster_data.rio.crs,
            shape=(
                int(raster_data.shape[1] * 10),  
                int(raster_data.shape[2] * 10)  
            ),
            resampling=Resampling.bilinear
        )
        resampled_raster_path = 'working_etccdi_file_resampled.tif'
        resampled_raster.rio.to_raster(resampled_raster_path)
        print(f"Resampled GeoTIFF saved at: {resampled_raster_path}")

        # Calculate zonal statistics
        gdf = gpd.read_file(param_shapefile_path)
        gdf = gdf[['gid', 'geometry', 'xcoord', 'ycoord']]
        stats = zonal_stats(gdf, resampled_raster_path, stats='mean', geojson_out=True)
        stats_gdf = gpd.GeoDataFrame.from_features(stats)

        # Add Year and Month fields to stats_gdf
        stats_gdf['year'] = year
        stats_gdf['month'] = month
        
        # Rename the 'mean' column to the climate index name
        stats_gdf.rename(columns={'mean': param_climate_index}, inplace=True)
        
        # Append the stats_gdf to the all_stats list
        all_stats.append(stats_gdf)

    # After the loop, concatenate all DataFrames into one
    final_gdf = pd.concat(all_stats, ignore_index=True)

    # Construct the output filename with the first and last date
    first_date_time = str(param_netcdf['time'].isel(time=first_time_index).values.item())
    last_date_time = str(param_netcdf['time'].isel(time=last_time_index).values.item())
    first_year, first_month = first_date_time.split('-')[0], first_date_time.split('-')[1]
    last_year, last_month = last_date_time.split('-')[0], last_date_time.split('-')[1]
    
    # Define the output path
    folder = 'etccdi_out_files'
    os.makedirs(folder, exist_ok=True)
    output_file_path = os.path.join(folder, f"{param_climate_index}_{first_year}_{first_month}__{last_year}_{last_month}.csv")
    
    # Save the final DataFrame to a CSV file
    final_gdf.to_csv(output_file_path, index=False)
    print(f"Final DataFrame saved to: {output_file_path}")
