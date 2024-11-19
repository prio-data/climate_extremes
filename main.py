import sys
import os

import sys
print("Python executable being used:", sys.executable)


import pandas as pd


from setup_environment import setup_utils_path
setup_utils_path()

# Format API Request ----------------------------------------------------------------
from unzip import unzip_etccdi_package
from correct_longitude import transform_longitudinal_values
from temporal_index import find_etccdi_timeindex, translate_index_to_daterange
from define_request import generate_and_validate_request

# Provide Metadata ------------------------------------------------------------------
from give_metadata import give_metadata

# Build API Request -----------------------------------------------------------------
from cds_api_pull import pull_from_cds_api

# Methods ---------------------------------------------------------------------------
from etccdi_to_pg__pointquery import generate_etccdi_temporal_tables__centroid
from etccdi_to_pg import generate_etccdi_temporal_tables

# Validation ------------------------------------------------------------------------
from give_reference_frame import provide_reference_frame
from id_null_values import report_null_etccdi_values

# Prompt the user for input
p_variable = input("Enter variable (e.g., 'consecutive_dry_days'): ")
p_product_type = input("Enter product type (e.g., 'base_independent'): ")
p_experiment = input("Enter experiment (e.g., 'ssp2_4_5'): ")
p_temporal_aggregation = input("Enter temporal aggregation (e.g., 'yearly'): ")

# Define Start Year & Month
start_year = input("Enter start year (e.g., '2015'): ")
start_month = input("Enter start month (e.g., '01'): ")

# Define End Year & Month
end_year = input("Enter end year (e.g., '2018'): ")
end_month = input("Enter end month (e.g., '04'): ")

# Method for processing
method = input("Enter method (e.g., 'resample'): ")

# Method for processing
save_raster_decision = input("Do you want to save each output raster file? (yes/no): ").lower()

if save_raster_decision == 'yes':
    raster_confirmation = input("Are you sure? Type 'YES' to confirm: ").upper()
    if raster_confirmation == 'YES':
        print("You have confirmed to save the raster files.")
        # Add your code to save the raster files here
    else:
        print("Raster files will not be saved.")
else:
    print("Raster files will not be saved.")

# Print out the values entered by the user to confirm
print(f"Parameters received:")
print(f"Variable: {p_variable}")
print(f"Product Type: {p_product_type}")
print(f"Experiment: {p_experiment}")
print(f"Temporal Aggregation: {p_temporal_aggregation}")
print(f"Start Year: {start_year}, Start Month: {start_month}")
print(f"End Year: {end_year}, End Month: {end_month}")
print(f"Method: {method}")
print(f'Decision to save individual raster files: {raster_confirmation}')