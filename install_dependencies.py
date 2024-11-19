import subprocess
import sys

def install_packages():
    """
    Installs the required Python packages for the project.
    """
    # List of required packages
    required_packages = [
        "rasterstats",   # Example: for raster operations
        "cdsapi",        # Example: for accessing Copernicus Climate Data Store API
        "numpy",         # Example: for numerical operations
        "pandas",        # Example: for data manipulation
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
