import pandas as pd 
from pathlib import Path

#from ingester3.extensions import *

def find_etccdi_timeindex(specified_year, specified_month, ds):
    """
    Finds the index of a specified month in a specified year in a NetCDF dataset.
    If the exact month is not found, it locates the index of the first month found in that year.

    Parameters:
        specified_year (str): The year to search for (e.g., '1990').
        specified_month (str): The month to search for (e.g., '01' for January).
        ds: The NetCDF dataset to search through.

    Returns:
        None
    """
    # Extract the time coordinate
    time_values = ds['time'].values  # Get the time coordinate values
    # Convert to string format to extract year and month
    time_strings = [str(t) for t in time_values]

    # Initialize variables to track indices and found months
    specified_month_index = None
    first_month_index = None

    # Search for any month in the specified year
    for idx, date in enumerate(time_strings):
        year, month, _ = date.split('-')  # Split to get year and month
        if year == specified_year:
            # Track the first month found
            if first_month_index is None:
                first_month_index = idx
            
            # Check for the specified month
            if month == specified_month:
                specified_month_index = idx  # Store the specified month index
                break  # Break immediately if specified month is found

    # Validate the results
    if specified_month_index is not None:
        # Confirm that the index corresponds to the specified month
        year_check, month_check, _ = time_strings[specified_month_index].split('-')
        print(f"Index of {specified_month} data for year {specified_year}: {specified_month_index}")
        print(f"Validation: Found data for Year: {year_check}, Month: {month_check} at index {specified_month_index}.")
        return(specified_month_index, month_check, year_check)
    else:
        # If the specified month data is not found, check if any month data exists
        if first_month_index is not None:
            print(f"No data found for {specified_month} of the year {specified_year} but located data for the first available month.")
            # Validate the first month found
            year_check, month_check, _ = time_strings[first_month_index].split('-')
            print(f"Validation: Found data for Year: {year_check}, Month: {month_check} at index {first_month_index}.")
            return(first_month_index, month_check, year_check)

        else:
            print(f"No data found for the year {specified_year}.")
            return(None)
        

def translate_index_to_daterange(etccdi, reference_df, temporal_res, start_year, start_month, end_year, end_month):

    
    project_root = Path(__file__).resolve().parent.parent

    ref_shapefile_path = project_root / 'data' / 'processed' / 'extent_shapefile' 


    #-----------------------------------------------------------
    # Establish Start and End index values:
    start_index_val, loc_start_month, loc_start_year =  find_etccdi_timeindex(start_year, start_month, etccdi)
    print()
    end_index_val, loc_end_month, loc_end_year = find_etccdi_timeindex(end_year, end_month, etccdi)
    print()
    #-----------------------------------------------------------
    print(f'The start index is: {start_index_val}, and references {loc_start_month} (month) of {loc_start_year} (year)')
    print()
    print(f'The end index is: {end_index_val}, and references {loc_end_month} (month) of {loc_end_year} (year)')
    print()
    #-----------------------------------------------------------
    index_list = list(range(start_index_val, end_index_val + 1))
    #-----------------------------------------------------------

    #-----------------------------------------------------------
    # Filter the PG reference file to the temporal parameters now established:
    #-----------------------------------------------------------

    # For annual:
    # the etccdi dataframe will contain a month field but this is irrelevant because the temporal resolution is 1-year
    if temporal_res == 'yearly':

        reference_filtered_time = reference_df.loc[(reference_df['year'] >= int(loc_start_year)) & (reference_df['year'] <= int(loc_end_year))]
        start_yyyy = str(loc_start_year) + str(loc_start_month).zfill(2)
        end_yyyy = str(loc_end_year) + str(loc_end_month).zfill(2)

        report_temporal_dimensions = [temporal_res, start_yyyy, end_yyyy]


    # For monthly:
    # why don't you filter for a monthly attribute?: Because all months will be included when subsetting by year.
    else:
    
        reference_filtered_time = reference_df.loc[
        ((reference_df['year'] == int(loc_start_year)) & (reference_df['month'] >= int(loc_start_month))) &
        ((reference_df['year'] == int(loc_end_year)) & (reference_df['month'] <= int(loc_end_month)))
    ]
    #-----------------------------------------------------------
        start_yyyymm = str(loc_start_year) + str(loc_start_month).zfill(2)

        end_yyyymm = str(loc_end_year) + str(loc_end_month).zfill(2)

        report_temporal_dimensions = [temporal_res, start_yyyymm, end_yyyymm]


    #print(reference_filtered_time)
    return(index_list, reference_filtered_time, report_temporal_dimensions)