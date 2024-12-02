import pandas as pd
from pathlib import Path

import geopandas as gpd
import pandas as pd
from shapely.geometry import Polygon
import os 


# Define the function to create a 0.5x0.5 degree grid cell around a center point
def create_grid_cell(lat, lon, cell_size=0.5):
    half_size = cell_size / 2
    # Define the corners of the grid cell
    return Polygon([
        (lon - half_size, lat - half_size),  # Bottom-left
        (lon + half_size, lat - half_size),  # Bottom-right
        (lon + half_size, lat + half_size),  # Top-right
        (lon - half_size, lat + half_size),  # Top-left
        (lon - half_size, lat - half_size)   # Close the polygon
    ])

from ingester3.extensions import *

def provide_reference_frame(temporal_aggregation_value):

    project_root = Path(__file__).resolve().parent.parent

    #--------------------------------------
    # Location to save geodataframe (as shapefile)
    #--------------------------------------

    ref_table_path = project_root / 'data' / 'processed' / 'reference_table'

    ref_shapefile_path = project_root / 'data' / 'processed' / 'extent_shapefile' 

    #temporal_aggregation_value = param_request['temporal_aggregation'][0]


# ----------------------------------------------------------------------------------------------------
    # ------------------------
    # Construct PG scaffolder
    # ------------------------

    #add a print() line when building the scaffolders as this may take several minutes
    print()
    print('Generating empty PG scaffolders which will be used to validate the spatial and temporal completeness of the selected indice.')
    print('This is expected to take several minutes...')
    print()
    pg = pd.DataFrame.pg.new_structure()

    pg['lat'] = pg.pg.lat
    pg['long'] = pg.pg.lon

    geometry = pg.apply(lambda row: create_grid_cell(row['lat'], row['long']), axis=1)
    gdf = gpd.GeoDataFrame(pg, geometry=geometry, crs="EPSG:4326")
    # ------------------------
    # WHY DO DO FOLLOW THIS ORDER:
    # apply lat and long first 
    gdf.to_file(f"{ref_shapefile_path}/pg_viewser_extent.shp")  # Save as a shapefile if needed
    # ------------------------
# ----------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------
    # ------------------------
    # Construct PGMonth scaffolder
    # ------------------------
    pgm = pd.DataFrame.pgm.new_structure()
    # ------------------------
    pgm['month'] = pgm.m.month
    pgm['year'] = pgm.m.year
    pgm = pgm.drop(columns=['month_id', 'pgm_id']).drop_duplicates()
# ----------------------------------------------------------------------------------------------------

    if temporal_aggregation_value == 'yearly':

        pgy = pgm.drop(columns=['month']).drop_duplicates()
        return(pgy)


    else:

        return(pgm)
