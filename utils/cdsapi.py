import cdsapi
from pathlib import Path


def pull_from_cds_api(request):
    # Define dataset and request parameters
    dataset = "sis-extreme-indices-cmip6"

    # Extract the desired elements from the request dictionary
    variable = request["variable"][0]
    temporal_aggregation = request["temporal_aggregation"][0]
    period = request["period"][0]

    # Concatenate them with an underscore to form the file name
    zip_file_name = f"{variable}_{temporal_aggregation}_{period}.zip"

    # Set the folder where you want to save the file (e.g., 'data/downloads')
    save_folder = Path("data") / "downloads"
    save_folder.mkdir(parents=True, exist_ok=True)  # Create the directory if it doesn't exist

    # Combine the folder path and the file name to create the full path
    zip_file_path = save_folder / zip_file_name

    # Initialize the client and retrieve the file
    client = cdsapi.Client()
    client.retrieve(dataset, request, target=str(zip_file_path)) 