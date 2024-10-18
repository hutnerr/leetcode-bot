import requests

URL = "https://leetcode.com/graphql"

def performQuery(query: str, variables: dict):
    response = requests.post(URL, json={'query': query, 'variables': variables})
    return response.json()