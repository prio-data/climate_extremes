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

# Data for the DataFrame
data_api = {
    "product_type": [
        "base_independent", "base_independent", "base_independent", "base_independent",
        "base_independent", "base_independent", "base_independent", "base_independent",
        "base_independent", "base_independent", "base_independent", "base_independent",
        "base_independent", "base_independent", "base_independent", "base_independent",
        "base_independent", "base_independent", "base_independent", "base_period_1961_1990",
        "base_period_1961_1990", "base_period_1961_1990", "base_period_1961_1990"
    ],
    "variable": [
        "consecutive_dry_days", "consecutive_wet_days", "diurnal_temperature_range", "frost_days",
        "growing_season_length", "heavy_precipitation_days", "ice_days", "maximum_1_day_precipitation",
        "maximum_5_day_precipitation", "maximum_value_of_daily_maximum_temperature",
        "minimum_value_of_daily_maximum_temperature", "maximum_value_of_daily_minimum_temperature",
        "minimum_value_of_daily_minimum_temperature", "number_of_wet_days", "simple_daily_intensity_index",
        "summer_days", "total_wet_day_precipitation", "tropical_nights", "very_heavy_precipitation_days",
        "cold_days", "cold_nights", "warm_days", "warm_nights"
    ],
    "temporal_aggregation": [
        "annual", "annual", "monthly or annual", "annual", "annual", "annual", "annual", "monthly or annual",
        "monthly or annual", "monthly or annual", "monthly or annual", "monthly or annual", "monthly or annual",
        "annual", "annual", "annual", "annual", "annual", "annual", "monthly or annual", "monthly or annual",
        "monthly or annual", "monthly or annual"
    ]
}


def safe_input(prompt):
    user_input = input(prompt)
    if user_input.lower() == 'quit':
        print("Exiting the script.")
        exit()
    return user_input


# Define the DataFrame
df_api = pd.DataFrame(data_api)

# Get temporal aggregation
print()
print("You will be prompted to provide a series of parameters to generate an API request for retrieving data from the Copernicus Data Store.\n If you make a mistake or wish to exit and review the README file for more information, simply type 'quit' at any prompt.")
print()
p_temporal_aggregation = safe_input("First, select a temporal aggregation ('yearly' / 'monthly'): ")

if p_temporal_aggregation == 'monthly':
    variable_list = df_api.loc[df_api['temporal_aggregation'].str.contains('monthly or annual'), 'variable'].tolist()
    print()
    p_variable = safe_input(f'Select indices are available at a monthly temporal resolution. Select from the following list ({variable_list}): ')
    print()
elif p_temporal_aggregation == 'yearly':
    variable_list = df_api['variable'].tolist()
    print()
    p_variable = safe_input(f'All variables are available at yearly temporal resolution. Here is a list of all available climate indices  ({variable_list}): ')
    print()
else:
    raise ValueError(f"Invalid temporal aggregation: '{p_temporal_aggregation}'. Please choose 'yearly' or 'monthly'.")

# Validate the variable selection
if p_variable in variable_list:
    print(f"'{p_variable}' is a valid selection.")
    print()
else:
    raise ValueError(f"'{p_variable}' is not in the list. Please check your spelling!")

# Define the product type
p_product_type = df_api.loc[df_api['variable'] == p_variable, 'product_type'].values[0]

# Get experiment
p_experiment = safe_input("Finally, select the climate experiment used to process the derived climate indices. Select from ('historical', 'ssp1_2_6', 'ssp2_4_5', or 'ssp5_8_5'): ")
print()
# Determine the period
if p_experiment == "historical" and p_temporal_aggregation == "monthly":
    p_period = "185001_201412"
elif p_experiment == "historical" and p_temporal_aggregation == "yearly":
    p_period = "1850_2014"
elif p_experiment in ["ssp1_2_6", "ssp2_4_5", "ssp5_8_5"] and p_temporal_aggregation == "monthly":
    p_period = "201501_210012"
elif p_experiment in ["ssp1_2_6", "ssp2_4_5", "ssp5_8_5"] and p_temporal_aggregation == "yearly":
    p_period = "2015_2100"
else:
    raise ValueError(f"Invalid combination of scenario '{p_experiment}' and time '{p_temporal_aggregation}'.")

# # Read configuration from the .txt file
# config_file_path = f'{base_dir}/request.txt'  # Adjust this path to where your .txt file is located

# config = {}
# with open(config_file_path, 'r') as file:
#     for line in file:
#         key, value = line.strip().split(': ')
#         config[key.strip()] = value.strip()

# # Assign variables from the config dictionary
# p_variable = config.get('p_variable')
# p_product_type = config.get('p_product_type')
# p_experiment = config.get('p_experiment')
# p_temporal_aggregation = config.get('p_temporal_aggregation')

# # Prompt the user for input
# p_variable = input("Enter variable (e.g., 'consecutive_dry_days'): ")
# p_product_type = input("Enter product type (e.g., 'base_independent'): ")
# p_experiment = input("Enter experiment (e.g., 'ssp2_4_5'): ")
# p_temporal_aggregation = input("Enter temporal aggregation (e.g., 'yearly'): ")

# Define Start Year & Month

# Split the string by the underscore
split_period = p_period.split('_') 

# Extract the first four characters of each element and convert them to integers
min_value = int(split_period[0][:4])  # First four characters, converted to integer
max_value = int(split_period[1][:4])  # First four characters, converted to integer

while True:
    # Define the user input (this will be from an input prompt)
    start_year = safe_input(f"Enter a start year between {min_value} and {max_value}: ")
    
    try:
        # Convert the user input to an integer
        start_year_int = int(start_year)

        # Check if the input is within the range
        if min_value <= start_year_int <= max_value:
            #print(f"The input value {start_year_int} is within the range {min_value}-{max_value}.")
            break  # Exit the loop if the input is valid
        else:
            print(f"The input value {start_year_int} is out of the permitted range {min_value}-{max_value}. Please try again.")

    except ValueError:
        print("Invalid input. Please enter a valid number.")


while True:
    # Define the user input (this will be from an input prompt)
    start_month = safe_input(f"Enter a start month between 01 and 12, use a two digit format (ie. 02, 03): ")
    
    try:
        # Convert the user input to an integer
        start_month_int = int(start_month)

        # Check if the input is within the range
        if 1 <= start_month_int <= 12:
            #print(f"The input value {start_month_int} is within the desired range.")
            break  # Exit the loop if the input is valid
        else:
            print(f"The input value {start_month_int} is out of the permitted range 01 - 12. Please try again.")

    except ValueError:
        print("Invalid input. Please enter a valid number.")

# Define End Year & Month

while True:

    # Define the user input (this will be from an input prompt)
    end_year = safe_input(f"Enter an end year between {min_value} and {max_value}: ")
    
    try:
        # Convert the user input to an integer
        end_year_int = int(end_year)

        # Check if the input is within the range
        if min_value <= end_year_int <= max_value:
            break  # Exit the loop if the input is valid
        else:
            print(f"The input value {end_year_int} is out of the permitted range {min_value}-{max_value}. Please try again.")

    except ValueError:
        print("Invalid input. Please enter a valid number.")


while True:
    # Define the user input (this will be from an input prompt)
    end_month = safe_input(f"Enter start month between 01 and 12, use a two digit format (ie. 02, 03): ")
    
    try:
        # Convert the user input to an integer
        end_month_int = int(end_month)

        # Check if the input is within the range
        if 1 <= end_month_int <= 12:
            #print(f"The input value {end_month_int} is within the desired range.")
            break  # Exit the loop if the input is valid
        else:
            print(f"The input value {end_month_int} is out of the permitted range 01 - 12. Please try again.")

    except ValueError:
        print("Invalid input. Please enter a valid number.")


print()
# Method for processing
method = safe_input("Enter method (raster_query / resample) ")
print()
# Method for processing
save_raster_decision = safe_input("Do you want to save each output raster file? (yes/no): ").lower()

if save_raster_decision == 'yes':
    raster_confirmation = safe_input("Are you sure? Type 'YES' to confirm: ").upper()
    if raster_confirmation == 'YES':
        print("You have confirmed to save the raster files.")
        # Add your code to save the raster files here
    else:
        print("Raster files will not be saved.")
        save_raster_decision = 'no'
else:
    print("Raster files will not be saved.")
    save_raster_decision = 'no'


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
    translated_filename = generate_etccdi_temporal_tables(index_list, etccdi, etccdi_index, report_temporal_dimensions, save_raster_decision)

else: 
    print('you have entered a bad prompt for the method parameter. Please restart.... ')

report_null_etccdi_values(translated_filename, reference_filtered_time, p_temporal_aggregation)