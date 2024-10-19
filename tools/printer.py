"""
Simple print functions to make debugging easier

Functions: 
    - printDict(dictionary: dict) -> None
    - printList(myList: list) -> None
    - printJSON(data: dict) -> None
    - printDatabaseRows(table: str) -> None
"""
import json

from tools import database_helper as dbh

def printDict(dictionary: dict) -> None:
    """
    Print a dictionary in a readable format
    Args:
        dictionary (dict): The dict to print
    """
    print('{')
    for key, value in dictionary.items():
        print("\t" + key, ":", value)
    print('}')
    
def printList(myList: list) -> None:
    """
    Iterate over and print a list in a readable format
    Args:
        myList (list): The list to print 
    """
    for item in myList:
        print(item)
        
def printJSON(data: dict) -> None:
    """
    Print a json object in a readable format
    Args:
        data (dict): The JSON object to print
    """
    print(json.dumps(data, indent=4))
    
def printDatabaseRows(table: str) -> None:
    """
    Print all rows in a database table
    Args:
        table (str): The table to print. Use tools.consts.DatabaseTables
    """
    rows = dbh.getRows(table)
    for row in rows:
        print(row)