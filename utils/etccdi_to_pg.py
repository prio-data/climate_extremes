import rioxarray
import rasterio
from rasterio.enums import Resampling
import matplotlib.pyplot as plt
import os
import geopandas as gpd
from rasterstats import zonal_stats
import pandas as pd
import numpy as np

def generate_etccdi_temporal_tables(param_time_index_list, param_netcdf, param_climate_index, param_shapefile_path):
    all_stats = []

    # Retrieve the first and last time indices for file naming
    first_time_index = param_time_index_list[0]
    last_time_index = param_time_index_list[-1]

    for i in param_time_index_list:
        print(f"Processing time index: {i}")
        
        # Select the data for the specified climate index
        data = param_netcdf[param_climate_index]
        
        # Check the data type and process accordingly
        data_type = data.dtype
        if data_type == 'timedelta64[ns]':
            data_days = data / np.timedelta64(1, 'D')  # Convert to days if it's timedelta
            raster_data = data_days.isel(time=i)
        elif data_type == 'float32':
            raster_data = data.isel(time=i)  # Use as-is if it's already float32
        else:
            raise TypeError(f"Unsupported data type '{data_type}' for variable '{param_climate_index}'. Expected 'timedelta64[ns]' or 'float32'.")
        
        # Plotting and other processing steps
        plt.figure(figsize=(10, 6))
        raster_data.plot(cmap='viridis')
        plt.title(f'{param_climate_index} at Time Index {i}')
        plt.xlabel('Longitude')
        plt.ylabel('Latitude')
        plt.show()

        # Convert spatial dimensions
        raster_data = raster_data.rename({'lon': 'x', 'lat': 'y'})
        raster_data = raster_data.rio.set_spatial_dims(x_dim='x', y_dim='y')

        # Get the date and time information
        date_time = str(param_netcdf['time'].isel(time=i).values.item())
        year = date_time.split('-')[0]
        month = date_time.split('-')[1]
        print("Year:", date_time)

        # Set CRS if not already defined
        if not raster_data.rio.crs:
            raster_data = raster_data.rio.write_crs("EPSG:4326")

        # Convert to float for consistent data type in raster operations
        raster_data = raster_data.astype('float32')

        # Check for NaN values and mask if needed
        raster_data = raster_data.where(~np.isnan(raster_data), other=0)  # Set NaNs to 0 for plotting
        
        # Save the raster to GeoTIFF
        raster_file_path = 'working_etccdi_file.tif'
        raster_data.rio.to_raster(raster_file_path)
        print(f"GeoTIFF saved at: {raster_file_path}")

        # Resample Raster
        raster_data = rioxarray.open_rasterio(raster_file_path)

        # Calculate current and new resolutions
        current_resolution_x = abs(raster_data.x[1] - raster_data.x[0])
        current_resolution_y = abs(raster_data.y[1] - raster_data.y[0])
        new_resolution_x = current_resolution_x / 10
        new_resolution_y = current_resolution_y / 10

        # Resample without introducing NoData values
        resampled_raster = raster_data.rio.reproject(
            raster_data.rio.crs,
            shape=(
                int(raster_data.shape[1] * 10),  
                int(raster_data.shape[2] * 10)  
            ),
            resampling=Resampling.bilinear
        )
        
        # Save resampled raster
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
        stats_gdf.rename(columns={'mean': param_climate_index}, inplace=True)

        # Plot the zonal statistics
        fig, ax = plt.subplots(figsize=(10, 6))
        stats_gdf.plot(column=param_climate_index, ax=ax, legend=True, cmap='viridis', edgecolor='none')
        ax.set_title(f'{param_climate_index} Statistics by Region - {year}-{month}')
        ax.set_xlabel('Longitude')
        ax.set_ylabel('Latitude')
        plt.show()

        # Append the stats_gdf to the all_stats list
        all_stats.append(stats_gdf)

    # Concatenate all DataFrames into one
    final_gdf = pd.concat(all_stats, ignore_index=True)

    # Construct the output filename
    first_date_time = str(param_netcdf['time'].isel(time=first_time_index).values.item())
    last_date_time = str(param_netcdf['time'].isel(time=last_time_index).values.item())
    first_year, first_month = first_date_time.split('-')[0], first_date_time.split('-')[1]
    last_year, last_month = last_date_time.split('-')[0], last_date_time.split('-')[1]
    
    # Save the final DataFrame to a CSV file
    folder = 'etccdi_out_files'
    os.makedirs(folder, exist_ok=True)
    output_file_path = os.path.join(folder, f"{param_climate_index}_{first_year}_{first_month}__{last_year}_{last_month}.csv")
    
    final_gdf.to_csv(output_file_path, index=False)
    print(f"Final DataFrame saved to: {output_file_path}")
