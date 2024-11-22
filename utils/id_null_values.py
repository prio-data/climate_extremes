import pandas as pd
from pathlib import Path


#Parameters:
# 1: validate_etccdi
# 2: reference_filtered_time
def report_null_etccdi_values(etccdi_pg_file, param_reference_filtered_time, temporal_aggregation_value):

    project_root = Path(__file__).resolve().parent.parent

    generated_index_table_folder = project_root / 'data' / 'generated' / 'index_table_output'
    find_file_path = generated_index_table_folder / etccdi_pg_file


    index = str(etccdi_pg_file).split('_')[0]
    #------------------------------------------------------------------------------------
    #load the developed Climate index 
    #------------------------------------------------------------------------------------
    validate_etccdi = pd.read_csv(find_file_path)
    #------------------------------------------------------------------------------------
    if temporal_aggregation_value == 'month':
        validate_etccdi['date'] = validate_etccdi['year'].astype(str) + '-' + validate_etccdi['month'].astype(str).str.zfill(2)
        validate_etccdi['year'] = validate_etccdi['year'].astype(str)


        param_reference_filtered_time['date'] = param_reference_filtered_time['year'].astype(str) + '-' + validate_etccdi['month'].astype(str).str.zfill(2)
    
        join_field = 'date'
    else:

        join_field = 'year'

    #etccdi_time_length = len(pd.unique(validate_etccdi['date']))
    #etccdi_spatial_length = len(pd.unique(validate_etccdi['gid']))
    #------------------------------------------------------------------------------------

    #------------------------------------------------------------------------------------
    # Perform a left join on the 'priogrid_gid' and 'gid' columns, and 'year'
    #------------------------------------------------------------------------------------
    merged_df = param_reference_filtered_time.merge(
        validate_etccdi,
        how='left',  # Keeps all rows from reference_filtered_time
        left_on=['priogrid_gid', join_field],  # Columns in reference_filtered_time
        right_on=['gid', join_field],  # Columns in validate_etccdi
        suffixes=('_reference', '_validate')  # Optional: Adds suffixes to distinguish overlapping columns
    )
    #------------------------------------------------------------------------------------
    # Check the result
    #print(merged_df.head())
    #------------------------------------------------------------------------------------

    #------------------------------------------------------------------------------------
    # Get a summary of the rows with NaN in the '<index>' field
    #------------------------------------------------------------------------------------
    total_nulls_validate = merged_df.isna().sum().sum()

    print(f"Total number of null values in 'validate_etccdi' DataFrame: {total_nulls_validate}")
    #------------------------------------------------------------------------------------

    #------------------------------------------------------------------------------------
    # Ask if there are na values located:
    #------------------------------------------------------------------------------------
    if total_nulls_validate != 0:

        #------------------------------------------------------------------------------------
        # Filter the merged DataFrame to find rows where the 'cddETCCDI' field is NaN
        null_cddETCCDI_rows = merged_df[merged_df[index].isna()]
        #------------------------------------------------------------------------------------

        # Group by 'year' and count NaN values in the 'Point_query_result' column
        nan_summary_df = null_cddETCCDI_rows.groupby(['year', 'month'])[index].apply(lambda x: x.isna().sum()).reset_index()

        # Rename columns for clarity
        nan_summary_df.columns = ['year', 'month', 'NaN_count']

        # Display the result
        print(nan_summary_df)
        #------------------------------------------------------------------------------------

    else:
        print(f"Total number of null values in 'validate_etccdi' DataFrame: {total_nulls_validate}")
        print('therefore, there is no null summary dataframe to report here!')