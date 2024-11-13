import zipfile
from pathlib import Path

def unzip_etccdi_package(param_zip_file_name):

    project_root = Path(__file__).resolve().parent.parent

    raw_data = project_root / 'data' / 'raw_external' / 'cds_zip'
    zip_file_path = raw_data / param_zip_file_name


    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        # Extract all contents to the current working directory
        zip_ref.extractall()  
        
        # Get the list of file names in the ZIP file
        netcdf_file = zip_ref.namelist()[0]  # This returns a list of file names in the ZIP


    # Split the filename on underscores
    parts = netcdf_file.split('_')

    # Keep only the first part
    etccdi_index = parts[0]
    # Optionally, delete the ZIP file after extraction
    #os.remove(zip_file_name)

    # Print the names of the extracted files
    print(etccdi_index)
    print("Extracted file names:", netcdf_file)
    return(netcdf_file, etccdi_index)