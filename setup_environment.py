# setup_environment.py
import sys
import os

def setup_utils_path():
    current_dir = os.getcwd()  # Get the current directory (should be repo root)
    utils_path = os.path.join(current_dir, 'utils')  # Relative path to utils folder
    if utils_path not in sys.path:
        sys.path.append(utils_path)  # Add utils folder to Python path
        print("Utils path added to Python Path:", utils_path)
    else:
        print("Utils path already in Python Path.")

if __name__ == "__main__":
    setup_utils_path()
