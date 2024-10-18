""" 
Simple helper file to perform a query on the leetcode graphql api

Functions:
    - performQuery(query: str, variables: dict) -> dict: 
"""
import requests

URL = "https://leetcode.com/graphql"

def performQuery(query: str, variables: dict) -> dict:
    """
    Perform a query on the leetcode graphql api
    Args:
        query (str): The query to perform. Use tools.consts.Query for the queries
        variables (dict): THe variables to pass to the query
    Returns:
        dict: The json response dict. 
    """
    response = requests.post(URL, json={'query': query, 'variables': variables})
    return response.json()