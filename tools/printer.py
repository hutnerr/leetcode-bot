import json
from tools import database_helper as dbh

def printDict(dictionary):
    print('{')
    for key, value in dictionary.items():
        print(key, ":", value)
    print('}')
    
def printList(myList):
    for item in myList:
        print(item)
        
def printJSON(data):
    print(json.dumps(data, indent=4))
    
def printDatabaseRows(table: str):
    rows = dbh.getRows(table)
    for row in rows:
        print(row)