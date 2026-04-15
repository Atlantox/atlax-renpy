import os
import zipfile
import sys

def get_base_path():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))

def get_resource_path(filename):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, filename)
    return os.path.join(os.path.abspath("."), filename)

def extract_zip(zip_name):
    base_path = get_base_path()
    zip_path = get_resource_path(zip_name)

    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(base_path)

    print("Atlax Renpy installacion ready!:", base_path)

if __name__ == "__main__":
    extract_zip("game.zip")
    input("Press any key to exit...")
