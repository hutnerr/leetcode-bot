import json
import os

fp = "data/serverdata/"
basefilepath = "data/serverdata/serverbase.json"

def newServerFile(sid):
    with open(basefilepath, 'r') as basefile:
        data = json.load(basefile)
        new_file_name = f"{fp}{sid}.json"
        data['id'] = sid
        with open(new_file_name, 'w') as new_file:
            json.dump(data, new_file)

def updateServerFile(sid, key1, key2, value):
    file_path = f"{fp}{sid}.json"
    data = getServerFile(sid)
    data[key1][key2] = value
    with open(file_path, 'w') as file:
        json.dump(data, file)

def getServerFile(sid):
    file_path = f"{fp}{sid}.json"
    if not os.path.exists(file_path):
        newServerFile(sid)
    with open(file_path, 'r') as file:
        return json.load(file)