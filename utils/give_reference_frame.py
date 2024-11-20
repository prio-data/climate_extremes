import pandas as pd
from pathlib import Path


def provide_reference_frame(param_request):

    project_root = Path(__file__).resolve().parent.parent

    ref_table_path = project_root / 'data' / 'processed' / 'reference_table' 

    temporal_aggregation_value = param_request['temporal_aggregation'][0]

    if temporal_aggregation_value == 'yearly':

        ref_table_file = ref_table_path / 'pg___y.csv'

        reference_df = pd.read_csv(ref_table_file)
        reference_df= reference_df.drop(columns=['Unnamed: 0'], errors='ignore')
    #-------------------------------------------------------------------
        # Convert 'year' to string
        #reference_df['year'] = reference_df['year'].astype(str)
    #-------------------------------------------------------------------
        print(reference_df.dtypes)
        return(reference_df)


    else:

        ref_table_file = ref_table_path / 'pg___m.csv'

        reference_df = pd.read_csv(ref_table_file)
        reference_df = reference_df.drop(columns=['Unnamed: 0'], errors='ignore')
    #-------------------------------------------------------------------
        # Convert 'year' to string
        #reference_df['year'] = reference_df['year'].astype(str)

        # Convert 'month' to an integer first (removes decimals) and then to string
        #reference_df['month'] = reference_df['month'].astype(int).astype(str)
    #-------------------------------------------------------------------
        print(reference_df.dtypes)
        return(reference_df)
