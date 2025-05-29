import json
from utils import file_helper as fh

# this module is util functions for working w/ JSON files
# readJSON: reads a JSON file and returns its content as a dictionary
# writeJSON: writes a dictionary to a JSON file
# updateJSON: updates a JSON file with new data, merging it with existing data

# reads a JSON file and returns its content as a dictionary
# returns None if the file does not exist
def readJSON(file_path: str) -> dict | None:
    if not fh.fileExists(file_path):
        return None
    
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)


def writeJSON(file_path: str, data: dict) -> bool:
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4)
        return True
    except Exception as e:
        print(f"Error writing JSON to {file_path}: {e}")
        return False


def updateJSON(file_path: str, data: dict) -> bool:
    existing_data = readJSON(file_path)
    if existing_data is None:
        return writeJSON(file_path, data)

    existing_data.update(data) # merge new data into existing data
    return writeJSON(file_path, existing_data)