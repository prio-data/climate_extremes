import sys
import os

import sys
print("Python executable being used:", sys.executable)


import pandas as pd
# Check the current directory before setup
base_dir= os.getcwd()
print(f"Current working directory before setup: {base_dir}")


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


# Read configuration from the .txt file
config_file_path = f'{base_dir}/request.txt'  # Adjust this path to where your .txt file is located

config = {}
with open(config_file_path, 'r') as file:
    for line in file:
        key, value = line.strip().split(':')
        config[key.strip()] = value.strip()

# Assign variables from the config dictionary
p_variable = config.get('p_variable')
p_product_type = config.get('p_product_type')
p_experiment = config.get('p_experiment')
p_temporal_aggregation = config.get('p_temporal_aggregation')

# # Prompt the user for input
# p_variable = input("Enter variable (e.g., 'consecutive_dry_days'): ")
# p_product_type = input("Enter product type (e.g., 'base_independent'): ")
# p_experiment = input("Enter experiment (e.g., 'ssp2_4_5'): ")
# p_temporal_aggregation = input("Enter temporal aggregation (e.g., 'yearly'): ")

# Define Start Year & Month
start_year = input("Enter start year (e.g., '2015'): ")
start_month = input("Enter start month (e.g., '01'): ")

# Define End Year & Month
end_year = input("Enter end year (e.g., '2018'): ")
end_month = input("Enter end month (e.g., '04'): ")

# Method for processing
method = input("Enter method (raster_query / resample) ")

# Method for processing
save_raster_decision = input("Do you want to save each output raster file? (yes/no): ").lower()

if save_raster_decision == 'yes':
    raster_confirmation = input("Are you sure? Type 'YES' to confirm: ").upper()
    if raster_confirmation == 'YES':
        print("You have confirmed to save the raster files.")
        # Add your code to save the raster files here
    else:
        print("Raster files will not be saved.")
        save_raster_decision = 'no'
else:
    print("Raster files will not be saved.")
    save_raster_decision = 'no'
# # Print out the values entered by the user to confirm
# print(f"Parameters received:")
# print(f"Variable: {p_variable}")
# print(f"Product Type: {p_product_type}")
# print(f"Experiment: {p_experiment}")
# print(f"Temporal Aggregation: {p_temporal_aggregation}")
# print(f"Start Year: {start_year}, Start Month: {start_month}")
# print(f"End Year: {end_year}, End Month: {end_month}")
# print(f"Method: {method}")
# print(f'Decision to save individual raster files: {save_raster_decision}')

request = generate_and_validate_request(
    variable=p_variable,
    product_type=p_product_type,
    experiment=p_experiment,
    temporal_aggregation=p_temporal_aggregation
)

print(request)

#-------------------------------------------------------------------
# Load a clean PG dataframe at a consistent temporal resolution
# to the request built
#-------------------------------------------------------------------

reference_df = provide_reference_frame(request)

zip_file_name = pull_from_cds_api(request)

netcdf_file, etccdi_index = unzip_etccdi_package(zip_file_name)

etccdi = transform_longitudinal_values(etccdi_index, netcdf_file)

print('Providing Metadata for the selected climate index:')
print()
give_metadata(etccdi)

index_list, reference_filtered_time, report_temporal_dimensions = translate_index_to_daterange(etccdi, reference_df, p_temporal_aggregation, start_year, start_month, end_year, end_month)

if method == 'raster_query':
    translated_filename = generate_etccdi_temporal_tables__centroid(index_list, etccdi, etccdi_index, report_temporal_dimensions, save_raster_decision)

elif method == 'resample':
    translated_filename = generate_etccdi_temporal_tables(index_list, etccdi, etccdi_index, save_raster_decision)

else: 
    print('you have entered a bad prompt for the method parameter. Please restart.... ')

report_null_etccdi_values(translated_filename, reference_filtered_time, p_temporal_aggregation)