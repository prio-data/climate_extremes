import subprocess
import sys

def install_packages():
    """
    Installs the required Python packages for the project.
    """
    # List of required packages
    required_packages = [
        'rasterstats'
        'cdsapi'
        'pandas'
        'numpy'
        'xarray'
        'rasterio'
        'geopandas'
        'matplotlib'
        'rioxarray'       # Example: for accessing Copernicus Climate Data Store API
        # Add any other required packages here
    ]

    # Install each package
    for package in required_packages:
        try:
            print(f"Installing {package}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        except subprocess.CalledProcessError:
            print(f"Failed to install {package}. Please check your configuration.")
    
    print("All required packages installed successfully!")

if __name__ == "__main__":
    install_packages()
