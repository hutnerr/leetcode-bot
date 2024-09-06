import json

# This file contains helper functions that make it easier to get
# the data out of the json file.

# The data.json file contains the bot key and the filepath for the directory

def openFile() -> dict:
    with open('data/data.json', 'r') as file:
        return json.load(file)
    
def key() -> str:
    return openFile()['key']

def filepath() -> str:
    return openFile()['filepath']

print(filepath())