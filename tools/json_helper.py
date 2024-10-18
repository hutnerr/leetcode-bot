import json

def getTitleSlug(json_data):
    return json_data['data']['challenge']['question']['titleSlug']

def get_json_keys(json_data):
    return json_data.keys()

def get_json_values(json_data):
    return json_data.values()

def printJson(json_data):
    print(json.dumps(json_data, indent=4, sort_keys=True))