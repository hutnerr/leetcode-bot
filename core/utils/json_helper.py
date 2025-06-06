import json
from core.utils import file_helper as fh

# reads a JSON file and returns its content as a dictionary
# returns None if the file does not exist
def readJSON(filePath: str) -> dict | None:
    if not fh.fileExists(filePath):
        return None
    
    with open(filePath, 'r', encoding='utf-8') as file:
        return json.load(file)

# writes a dictionary to a JSON file
def writeJSON(filePath: str, data: dict) -> bool:
    try:
        with open(filePath, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4)
        return True
    except Exception as e:
        print(f"Error writing JSON to {filePath}: {e}")
        return False

# updates a JSON file with new data, merging it w/ old data
def updateJSON(filePath: str, data: dict) -> bool:
    existingData = readJSON(filePath)
    if existingData is None:
        return writeJSON(filePath, data)

    existingData.update(data) # merge new data into existing data
    return writeJSON(filePath, existingData)