import math  # Add this import at the top of your file
import rasterio
import geopandas as gpd
import pandas as pd
import numpy as np
from rasterstats import point_query
import os
import matplotlib.pyplot as plt
from pathlib import Path
from matplotlib.backends.backend_pdf import PdfPages  # Import PdfPages for saving PDF layouts
import tempfile



def generate_layout_and_save(param_time_index_list, plot_figures, output_folder, param_climate_index):
    columns = 4
    rows = 3
    plots_per_page = columns * rows
    total_plots = len(plot_figures)
    total_pages = math.ceil(total_plots / plots_per_page)

    output_folder = Path(output_folder)
    output_folder.mkdir(parents=True, exist_ok=True)
    output_file = output_folder / f'{param_climate_index}_layout.pdf'

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


def generate_etccdi_temporal_tables__centroid(param_time_index_list, param_netcdf, param_climate_index, param_shapefile_name='pgm_viewser_extent.shp'):
    project_root = Path.cwd()  # Set this to your project root manually if needed
    extent_path = project_root / 'data' / 'processed' / 'extent_shapefile'
    extent_filename = extent_path / param_shapefile_name
    generated_index_table_folder = project_root / 'data' / 'generated' / 'index_table_output'
    
    map_folder = project_root / 'docs' / 'Graphics' / 'Standard_review'

    gdf = gpd.read_file(extent_filename)
    gdf = gdf[['gid', 'geometry', 'xcoord', 'ycoord']]

    all_stats = []
    plot_figures = []  # Initialize list to store figures

    for i in param_time_index_list:
        print(f"Processing time index: {i}")
        
        data = param_netcdf[param_climate_index]
        data_type = data.dtype

        if data_type == 'timedelta64[ns]':
            data_days = data / np.timedelta64(1, 'D')
            raster_data = data_days.isel(time=i)
        elif data_type == 'float32':
            raster_data = data.isel(time=i)
        else:
            raise TypeError(f"Unsupported data type '{data_type}' for variable '{param_climate_index}'.")

        raster_data = raster_data.rename({'lon': 'x', 'lat': 'y'})
        raster_data = raster_data.rio.set_spatial_dims(x_dim='x', y_dim='y')
        date_time = str(param_netcdf['time'].isel(time=i).values.item())
        year, month = date_time.split('-')[:2]
        print("Year:", year, "Month:", month)

        if not raster_data.rio.crs:
            print("CRS is not set. Setting CRS to EPSG:4326")
            raster_data = raster_data.rio.write_crs("EPSG:4326")

        temp_raster = f'temp_raster_{year}_{month}.tif'
        raster_data.rio.to_raster(temp_raster)

        gdf['centroid'] = gdf.geometry.centroid
        gdf[f'Point_query_result'] = point_query(
            gdf['centroid'],
            temp_raster,
            interpolate='nearest'
        )
        gdf = gdf.drop(columns=['centroid'])
        stats_gdf = gdf.copy()
        stats_gdf['year'] = year
        stats_gdf['month'] = month
        all_stats.append(stats_gdf)

        # Create and save the figure without displaying it

        fig, ax = plt.subplots(1, 1, figsize=(10, 8))
        stats_gdf.plot(column=f'Point_query_result', cmap='viridis', legend=True, ax=ax)
        ax.set_title(f"Raster Values for {year}-{month}")
        plt.xlabel("Longitude")
        plt.ylabel("Latitude")
        plt.show() 
        plot_figures.append(fig)  # Append figure to list

    final_gdf = pd.concat(all_stats, ignore_index=True)
    first_time_index = param_time_index_list[0]
    last_time_index = param_time_index_list[-1]

    stats_gdf.rename(columns={'Point_query_result': param_climate_index}, inplace=True)

    file_name = f"{param_climate_index}_{first_time_index}_{last_time_index}__centroid_process.csv"
    output_file_path = generated_index_table_folder / file_name
    final_gdf.to_csv(output_file_path, index=False)
    print(f"Final DataFrame saved to: {output_file_path}")
    print(file_name)

    # Save layout of all figures
    generate_layout_and_save(param_time_index_list, plot_figures, map_folder, param_climate_index)
    
    param_netcdf.close()
    return file_name
