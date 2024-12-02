import rioxarray
import numpy as np
import matplotlib.pyplot as plt
from rasterio.enums import Resampling
import xarray as xr
import geopandas as gpd
from rasterstats import zonal_stats
import pandas as pd
import os

import math  # Add this import at the top of your file
import geopandas as gpd


from pathlib import Path
from matplotlib.backends.backend_pdf import PdfPages  # Import PdfPages for saving PDF layouts
import tempfile

from rasterio.io import MemoryFile

def generate_layout_and_save(param_time_index_list, plot_figures, output_folder, param_climate_index):
    columns = 4
    rows = 3
    plots_per_page = columns * rows
    total_plots = len(plot_figures)
    total_pages = math.ceil(total_plots / plots_per_page)

    output_folder = Path(output_folder)
    output_folder.mkdir(parents=True, exist_ok=True)
    output_file = output_folder / f'{param_climate_index}_layout__resample.pdf'

    with PdfPages(output_file) as pdf:
        for page in range(total_pages):
            fig, axes = plt.subplots(rows, columns, figsize=(11.69, 8.27))  # A4 size in landscape
            axes = axes.flatten()

            for i in range(plots_per_page):
                plot_index = page * plots_per_page + i
                if plot_index < total_plots:
                    fig_plot = plot_figures[plot_index]
                    
                    # Remove x and y labels, but keep the axes and legend
                    for ax in fig_plot.get_axes():
                        ax.set_xlabel('')  # Remove x-axis label
                        ax.set_ylabel('')  # Remove y-axis label

                    # Save each figure to a temporary file, then load it
                    with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmpfile:
                        fig_plot.savefig(tmpfile.name, bbox_inches='tight')  # Save plot with legend
                        img = plt.imread(tmpfile.name)
                        axes[i].imshow(img)  # Place the image into the subplot axis
                        axes[i].axis('off')  # Turn off axis for a cleaner layout
                else:
                    axes[i].axis('off')  # Hide unused subplots

            plt.tight_layout()
            pdf.savefig(fig)
    plt.close(fig)

    print(f"All graphics saved to {output_file}")
    return output_file


def generate_etccdi_temporal_tables(param_time_index_list, param_netcdf, param_climate_index, temporal_params, save_raster, param_shapefile_name='pg_viewser_extent.shp'):
    project_root = Path.cwd()  # Set this to your project root manually if needed

    map_folder = project_root / 'docs' / 'Graphics' / 'Standard_review'

    extent_path = project_root / 'data' / 'processed' / 'extent_shapefile'
    extent_filename = extent_path / param_shapefile_name


    out_originalraster_folder = project_root / 'data' / 'generated' / 'index_raster_output' /'native' 
    out_upsampleraster_folder = project_root / 'data' / 'generated' / 'index_raster_output' / 'upsampled'

    generated_index_table_folder = project_root / 'data' / 'generated' / 'index_table_output'

    temporal_attribution = '_'.join(temporal_params)

    all_stats = []
    plot_figures = []  # Initialize list to store figures

    # Ensure the output folder exists
    #os.makedirs(output_folder, exist_ok=True)

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
        
        # Convert spatial dimensions
        raster_data = raster_data.rename({'lon': 'x', 'lat': 'y'})
        raster_data = raster_data.rio.set_spatial_dims(x_dim='x', y_dim='y')

        # Get the date and time information
        date_time = str(param_netcdf['time'].isel(time=i).values.item())
        year, month = date_time.split('-')[:2]
        print("Year:", year, "Month:", month)

        # Set CRS if not already defined
        if not raster_data.rio.crs:
            print("CRS is not set. Setting CRS to EPSG:4326")
            raster_data = raster_data.rio.write_crs("EPSG:4326")

        # Save the original raster to the designated folder
        # --- original_raster_path = os.path.join(out_originalraster_folder, f"original_{param_climate_index}_{year}_{month}.tif")
        # ---- raster_data.rio.to_raster(original_raster_path)
        # ---- print(f"Original raster saved at: {original_raster_path}")

        # Create a separate raster with null values set to -9999
        # --- raster_with_nulls_set = raster_data.fillna(-9999)

        # Save the modified raster (with nulls as -9999) to the designated folder
        # --- null_set_raster_path = os.path.join(out_originalraster_folder, f"null_set_{param_climate_index}_{year}_{month}.tif")
        # --- raster_with_nulls_set.rio.to_raster(null_set_raster_path)
        # --- print(f"Raster with nulls set to -9999 saved at: {null_set_raster_path}")

        # Resample directly with bilinear interpolation
        def resample_with_bilinear(raster_data, factor=3):
            # Resample with the target shape
            upsampled_raster = raster_data.rio.reproject(
                raster_data.rio.crs,
                shape=(
                    int(raster_data.sizes['y'] * factor),
                    int(raster_data.sizes['x'] * factor)
                ),
                resampling=Resampling.bilinear
            )
            return upsampled_raster

        # Apply the resampling method
        upsampled_raster = resample_with_bilinear(raster_data, factor=20)

        # Plot the resampled raster
        plt.figure(figsize=(10, 6))
        upsampled_raster.plot(cmap='viridis')
        plt.title(f'Upsampled Raster for {param_climate_index} at Time Index {i}')
        plt.xlabel('Longitude')
        plt.ylabel('Latitude')
        #plt.show()

        if save_raster == 'yes':
            upsampled_raster_path = os.path.join(out_upsampleraster_folder, f"upsampled_{param_climate_index}_{year}_{month}.tif")
            upsampled_raster.rio.to_raster(upsampled_raster_path)
            print(f"Upsampled raster saved at: {upsampled_raster_path}")
            
        else:
        # Save the resampled raster to the designated folder
            with MemoryFile() as memfile:
                with memfile.open(driver='GTiff', 
                                width=upsampled_raster.rio.width, 
                                height=upsampled_raster.rio.height, 
                                count=1, 
                                dtype=upsampled_raster.dtype, 
                                crs=upsampled_raster.rio.crs, 
                                transform=upsampled_raster.rio.transform()) as dataset:
                    dataset.write(upsampled_raster.values, 1)

                # Load the shapefile for zonal statistics
                gdf = gpd.read_file(extent_filename)

                # Calculate zonal statistics on the upsampled raster
                stats = zonal_stats(gdf, memfile, stats='mean', geojson_out=True)
                stats_gdf = gpd.GeoDataFrame.from_features(stats)

                # Add year and month fields
                stats_gdf['year'] = year
                stats_gdf['month'] = month
                stats_gdf.rename(columns={'mean': param_climate_index}, inplace=True)

                # Ensure stats_gdf has valid geometry and data
                stats_gdf = stats_gdf[stats_gdf.geometry.notnull() & stats_gdf[param_climate_index].notnull()]
            del upsampled_raster  # Clean up if no longer needed

        # Plot the zonal statistics if there is data
        if not stats_gdf.empty:
            fig, ax = plt.subplots(figsize=(10, 6))
            stats_gdf.plot(column=param_climate_index, ax=ax, legend=True, cmap='viridis', edgecolor='none')
            ax.set_title(f'{param_climate_index} Statistics by Region - {year}-{month}')
            ax.set_xlabel('Longitude')
            ax.set_ylabel('Latitude')
            #plt.show()
            plot_figures.append(fig)  # Append figure to list
            plt.close(fig)

        else:
            print(f"No valid zonal statistics data to plot for {param_climate_index} at time index {i}")

        # Append to list
        all_stats.append(stats_gdf)

    # Concatenate all DataFrames
    final_gdf = pd.concat(all_stats, ignore_index=True)

    # Save final DataFrame to CSV in the designated folder

    file_name = f"{param_climate_index}_{temporal_attribution}__centroid_process.csv"
    output_file_path = generated_index_table_folder / file_name


    final_gdf.to_csv(output_file_path, index=False)
    print(f"Final DataFrame saved to: {output_file_path}")

    generate_layout_and_save(param_time_index_list, plot_figures, map_folder, param_climate_index)

    return output_file_path