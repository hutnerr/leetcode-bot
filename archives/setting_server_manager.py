import json
import os

fp = "data/serverdata/"
basefilepath = "data/serverbase.json"

def newServerFile(sid):
    with open(basefilepath, 'r') as basefile:
        data = json.load(basefile)
        new_file_name = f"{fp}{sid}.json"
        data['id'] = sid
        with open(new_file_name, 'w') as new_file:
            json.dump(data, new_file)
    addToTimesFile('data/times/12.txt', sid)

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
    
def updateTimesFile(newtimefile, sid):
    pathfront = 'data/times/'

    oldtimefile = getServerFile(sid)['dailies']['hourfile']

    removeFromTimesFile(pathfront + oldtimefile, sid)
    addToTimesFile(pathfront + newtimefile, sid)

def addToTimesFile(path, sid):
    with open(path, 'a') as file:
        file.write(f"{sid}\n")

def removeFromTimesFile(path, sid):
    with open(path, 'r') as file:
        lines = file.readlines()

    print(f"{sid}\n")

    lines.remove(f"{sid}\n")
    with open(path, 'w') as file:
        file.writelines(lines)