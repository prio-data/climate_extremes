import pandas as pd

def provide_reference_frame(param_request):

    temporal_aggregation_value = param_request['temporal_aggregation'][0]

    if temporal_aggregation_value == 'yearly':
        reference_df = pd.read_csv('/Users/gbenz/Documents/Climate Data/climate_extremes/data/processed/pg__y.csv')
        reference_df= reference_df.drop(columns=['Unnamed: 0'], errors='ignore')
    #-------------------------------------------------------------------
        # Convert 'year' to string
        reference_df['year'] = reference_df['year'].astype(str)
    #-------------------------------------------------------------------
        print(reference_df.dtypes)
        return(reference_df)


    else:
        reference_df = pd.read_csv('/Users/gbenz/Documents/Climate Data/climate_extremes/data/processed/pg__m.csv')
        reference_df = reference_df.drop(columns=['Unnamed: 0'], errors='ignore')
    #-------------------------------------------------------------------
        # Convert 'year' to string
        reference_df['year'] = reference_df['year'].astype(str)

        # Convert 'month' to an integer first (removes decimals) and then to string
        reference_df['month'] = reference_df['month'].astype(int).astype(str)
    #-------------------------------------------------------------------
        print(reference_df.dtypes)
        return(reference_df)
