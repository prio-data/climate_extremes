import rasterio
import geopandas as gpd
import pandas as pd
import numpy as np
from rasterstats import point_query
import os
import matplotlib.pyplot as plt

def generate_etccdi_temporal_tables__centroid(param_time_index_list, param_netcdf, param_climate_index, param_shapefile_path, output_folder):


    # Load the finer grid (zones) as a GeoDataFrame
    gdf = gpd.read_file(param_shapefile_path)
    gdf = gdf[['gid', 'geometry', 'xcoord', 'ycoord']]

    # Initialize an empty list to hold the stats DataFrames
    all_stats = []

    # Loop through each time index in the NetCDF file
    for i in param_time_index_list:
        print(f"Processing time index: {i}")

        # Select data for the specified climate index and handle data types
        data = param_netcdf[param_climate_index]
        data_type = data.dtype

        if data_type == 'timedelta64[ns]':
            data_days = data / np.timedelta64(1, 'D')  # Convert to days if it's timedelta
            raster_data = data_days.isel(time=i)
        elif data_type == 'float32':
            raster_data = data.isel(time=i)
        else:
            raise TypeError(f"Unsupported data type '{data_type}' for variable '{param_climate_index}'.")

        # Convert spatial dimensions to be compatible with rasterio and zonal statistics
        raster_data = raster_data.rename({'lon': 'x', 'lat': 'y'})
        raster_data = raster_data.rio.set_spatial_dims(x_dim='x', y_dim='y')

        # Extract date and time information for labeling or file naming
        date_time = str(param_netcdf['time'].isel(time=i).values.item())
        year, month = date_time.split('-')[:2]
        print("Year:", year, "Month:", month)

        # Ensure CRS is set to EPSG:4326 if undefined
        if not raster_data.rio.crs:
            print("CRS is not set. Setting CRS to EPSG:4326")
            raster_data = raster_data.rio.write_crs("EPSG:4326")

        # Save the raster for the current time slice to a temporary GeoTIFF for zonal stats
        temp_raster = f'temp_raster_{year}_{month}.tif'
        raster_data.rio.to_raster(temp_raster)

        # Calculate centroids of each polygon in the shapefile for point-based sampling
        gdf['centroid'] = gdf.geometry.centroid

        # Use `point_query` to get raster values at each centroid
        gdf[f'Point_query_result'] = point_query(
            gdf['centroid'],  # Use centroids as the query points
            temp_raster,  # Temporary raster file
            interpolate='nearest'  # Nearest neighbor interpolation to match the coarse grid
        )

        # Remove the centroid column to avoid multiple geometry columns
        gdf = gdf.drop(columns=['centroid'])

        # Create a copy of the current gdf with the new raster value column
        stats_gdf = gdf.copy()

                # Add year and month fields
        stats_gdf['year'] = year
        stats_gdf['month'] = month
        #stats_gdf.rename(columns={'mean': param_climate_index}, inplace=True)

        # Append the current stats_gdf to the all_stats list
        all_stats.append(stats_gdf)

        # Plotting the shapefile with the interpolated raster values (optional)
        fig, ax = plt.subplots(1, 1, figsize=(10, 8))
        stats_gdf.plot(column=f'Point_query_result', cmap='viridis', legend=True, ax=ax)
        ax.set_title(f"Raster Values for {year}-{month}")
        plt.xlabel("Longitude")
        plt.ylabel("Latitude")
        plt.show()

    # Concatenate all DataFrames
    final_gdf = pd.concat(all_stats, ignore_index=True)

    # Define output CSV file path
    first_time_index = param_time_index_list[0]
    last_time_index = param_time_index_list[-1]
    output_file_path = os.path.join(output_folder, f"{param_climate_index}_{first_time_index}_{last_time_index}__centroid_process.csv")

    # Save the final DataFrame to CSV
    final_gdf.to_csv(output_file_path, index=False)
    print(f"Final DataFrame saved to: {output_file_path}")

    # Clean up: Close the dataset
    param_netcdf.close()

