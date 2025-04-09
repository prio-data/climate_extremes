import sys
import os

import sys
print("Python executable being used:", sys.executable)


import pandas as pd
# Check the current directory before setup
base_dir= os.getcwd()
print(f"Current working directory before setup: {base_dir}")


# Format API Request ----------------------------------------------------------------
from utils.unzip import unzip_etccdi_package
from utils.correct_longitude import transform_longitudinal_values
from utils.temporal_index import translate_index_to_daterange
from utils.define_request import generate_and_validate_request

# Provide Metadata ------------------------------------------------------------------
from utils.give_metadata import give_metadata

# Build API Request -----------------------------------------------------------------
from utils.cds_api_pull import pull_from_cds_api

# Methods ---------------------------------------------------------------------------
from utils.etccdi_to_pg__pointquery import generate_etccdi_temporal_tables__centroid
from utils.etccdi_to_pg import generate_etccdi_temporal_tables

# Validation ------------------------------------------------------------------------
from utils.give_reference_frame import provide_reference_frame
from utils.id_null_values import report_null_etccdi_values

# Global Statistics -----------------------------------------------------------------
from utils.global_summary_stats import report_summary_stats, plot_statistics

import click


EXPERIMENT_YEAR_RANGES = {
    "historical": (1850, 2014),
    "ssp1_2_6": (2015, 2100),
    "ssp2_4_5": (2015, 2100),
    "ssp5_8_5": (2015, 2100),
}

DATA_API = {
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




def get_variable_list(temporal_aggregation, df_api):
    if temporal_aggregation == "monthly":
        return df_api.loc[df_api['temporal_aggregation'].str.contains('monthly or annual'), 'variable'].tolist()
    elif temporal_aggregation == "yearly":
        return df_api["variable"].tolist()


def validate_temporal_aggregation(ctx, param, value):
    if value not in ["yearly", "monthly"]:
        raise click.BadParameter("Please choose 'yearly' or 'monthly'.")
    return value

def validate_variable(temporal_aggregation, variable):
    df_api = pd.DataFrame(DATA_API)  
    valid_vars = get_variable_list(temporal_aggregation, df_api)
    
    if variable not in valid_vars:
        raise click.BadParameter(f"'{variable}' is not available for {temporal_aggregation} aggregation.")
    return variable

def validate_experiment(ctx, param, value):
    valid_experiments = ["historical", "ssp1_2_6", "ssp2_4_5", "ssp5_8_5"]
    if value not in valid_experiments:
        raise ValueError(f"Invalid experiment. Choose from {valid_experiments}.")
    return value

def validate_years(experiment, start, end):
    start_int = int(start)
    end_int = int(end)

    if experiment is None:
        raise click.BadParameter("Experiment is required but not provided.")
    if experiment not in EXPERIMENT_YEAR_RANGES:
        raise click.BadParameter(f"Invalid experiment '{experiment}' provided.")
    
    min_year, max_year = EXPERIMENT_YEAR_RANGES[experiment]
    if not (min_year <= start_int <= max_year):
        raise click.BadParameter(f"Start year must be between {min_year} and {max_year} for {experiment}.")
    
    if not (min_year <= end_int <= max_year):
        raise click.BadParameter(f"End year must be between {min_year} and {max_year} for {experiment}.")
    
    if start_int >= end_int:
        raise click.BadParameter("Start year must be less than end year.")
    
    return start, end

def validate_months(temporal_aggregation, start_month, end_month):
    if temporal_aggregation == 'monthly':
        if start_month is None or end_month is None:
            raise click.BadParameter("Both start and end months must be specified when using monthly aggregation (valid range: 01-12).")
        try:
            start_month_int = int(start_month)
            end_month_int = int(end_month)
            if not (1 <= start_month_int <= 12):
                raise click.BadParameter(f"Start month must be between 1 and 12.")
            
            if not (1 <= end_month_int <= 12):
                raise click.BadParameter(f"End month must be between 1 and 12.")
            
            if start_month_int > end_month_int:
                raise click.BadParameter("Start month must be less than or equal to end month.")
        
        except ValueError:
            raise click.BadParameter("Month must be an integer between 1 and 12.")
    return start_month, end_month


def validate_method(ctx, param, value):
    valid_methods = ["raster_query", "resample"]
    if value not in valid_methods:
        raise click.BadParameter(f"Invalid method. Choose from {valid_methods}.")
    return value

def validate_save_raster(ctx, param, value):
    valid_choices = ["yes", "no"]
    if value not in valid_choices:
        raise click.BadParameter(f"Invalid option for save-raster. Choose from {valid_choices}.")
    return value


def get_variable_help():
    df_api = pd.DataFrame(DATA_API)
    monthly_vars = df_api.loc[df_api['temporal_aggregation'].str.contains('monthly or annual'), 'variable'].tolist()
    yearly_vars = df_api['variable'].to_list()
    message = """Choose a variable to process based on the temporal aggregation.

\b
Monthly variables:
- {}

\b
Yearly variables:
- {}
""".format("\n- ".join(monthly_vars), "\n- ".join(yearly_vars))

    return message




@click.command()
@click.option('--temporal-aggregation', type=click.Choice(['yearly', 'monthly']), default='yearly', callback=validate_temporal_aggregation,
              help="Temporal aggregation ('yearly' / 'monthly')")
@click.option(
    '--variable', default='cold_days', help=get_variable_help()
)
@click.option('--experiment', type=click.Choice(["historical", "ssp1_2_6", "ssp2_4_5", "ssp5_8_5"]), default='historical', callback=validate_experiment,
              help="Experiment type")
@click.option('--start-year', type=str, default='2000', help="Start year (depends on experiment)")
@click.option('--end-year', type=str, default='2001', help="End year (depends on experiment)")
@click.option('--start-month', type=str, default=None, help="Start month (01-12), required for monthly aggregation")
@click.option('--end-month', type=str, default=None, help="End month (01-12), required for monthly aggregation")
@click.option('--method', type=click.Choice(["raster_query", "resample"]), default='raster_query', callback=validate_method, help="Method to use")
@click.option('--save-raster', type=click.Choice(["yes", "no"]), default='no', callback=validate_save_raster, help="Save raster files? ('yes' or 'no')")
def main(temporal_aggregation, variable, experiment, start_year, end_year, start_month, end_month, method, save_raster):
    """CLI tool to generate API requests and process climate data."""
    validate_variable(temporal_aggregation, variable)
    validate_years(experiment, start_year, end_year)
    validate_months(temporal_aggregation, start_month, end_month)


    click.echo(f"Selected temporal aggregation: {temporal_aggregation}")
    click.echo(f"Selected variable: {variable}")
    click.echo(f"Experiment: {experiment}")
    click.echo(f"Start year: {start_year}")
    click.echo(f"End year: {end_year}")
    click.echo(f"Start month: {start_month}")
    click.echo(f"End month: {end_month}")
    click.echo(f"Method: {method}")
    click.echo(f"Save raster: {save_raster}")


    df_api = pd.DataFrame(DATA_API)
    product_type = df_api.loc[df_api['variable'] == variable, 'product_type'].values[0]

    request = generate_and_validate_request(
    variable=variable,
    product_type=product_type,
    experiment=experiment,
    temporal_aggregation=temporal_aggregation
    )

    print(request)
    

    zip_file_name = pull_from_cds_api(request)

    netcdf_file, etccdi_index = unzip_etccdi_package(zip_file_name)

    etccdi = transform_longitudinal_values(etccdi_index, netcdf_file)

    print('Providing Metadata for the selected climate index:')
    print()
    give_metadata(etccdi)

    reference_df = provide_reference_frame(temporal_aggregation)

    index_list, reference_filtered_time, report_temporal_dimensions = translate_index_to_daterange(etccdi, reference_df, temporal_aggregation, start_year, start_month, end_year, end_month)

    if method == 'raster_query':
        translated_filename = generate_etccdi_temporal_tables__centroid(index_list, etccdi, etccdi_index, report_temporal_dimensions, save_raster)

    elif method == 'resample':
        translated_filename = generate_etccdi_temporal_tables(index_list, etccdi, etccdi_index, report_temporal_dimensions, save_raster)


    report_null_etccdi_values(translated_filename, reference_filtered_time, temporal_aggregation)

    # Generate Global Summary Stats:
    df_an, df1, df2= report_summary_stats(translated_filename)
    plot_statistics(etccdi_index, df_an, df1, df2)
    
        
       
        
    


if __name__ == '__main__':
    
    
    main()
