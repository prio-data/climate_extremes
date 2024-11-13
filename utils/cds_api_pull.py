import cdsapi
from pathlib import Path


def pull_from_cds_api(request):

    project_root = Path(__file__).resolve().parent.parent

    raw_data = project_root / 'data' / 'raw_external' / 'cds_zip'

    # Define dataset and request parameters
    dataset = "sis-extreme-indices-cmip6"

    # Extract the desired elements from the request dictionary
    variable = request["variable"][0]
    temporal_aggregation = request["temporal_aggregation"][0]
    period = request["period"][0]

    # Concatenate them with an underscore to form the file name
    zip_file_name = f"{variable}_{temporal_aggregation}_{period}.zip"

    # Combine the folder path and the file name to create the full path
    zip_file_path = raw_data / zip_file_name

    # Initialize the client and retrieve the file
    client = cdsapi.Client()
    client.retrieve(dataset, request, target=str(zip_file_path)) 

    return(zip_file_name)