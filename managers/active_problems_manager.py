"""
Manages the active problems for a server

Functions: 
    - updateActiveProblems(serverID: int, problemID: int, slug: str) -> None
    - getActiveProblems(serverID:int ) -> tuple
    - parseActiveProblems(row: tuple) -> dict
    - getAndParseActiveProblems(serverID: int) -> dict
"""
from tools import database_helper as dbh
from tools.consts import DatabaseTables as dbt
from tools.consts import DatabaseFields as dbf

def updateActiveProblems(serverID: int, problemID: int, slug: str) -> None:
    """
    Update the active problems table with the new problem slug
    Args:
        serverID (int): The Discord server ID
        problemID (int): The ID of the problem to update
        slug (str): The slug of the new problem
    """
    # If we don't contain the serverID in the table, add it
    # I think this should be added to the setup script instead 
    # then perform a check to see if the server has setup to call it, if so, it should exist
    if not dbh.contains(dbt.ACTIVE_PROBLEMS.value, "serverID = ?", (serverID,)):
        dbh.addRow(dbt.ACTIVE_PROBLEMS.value, dbf.ACTIVE_PROBLEMS.value, (serverID, "none", "none", "none"))
    
    dbh.updateRow(dbt.ACTIVE_PROBLEMS.value, f'p{problemID}', slug, f'serverID = {serverID}')
    
def getActiveProblems(serverID:int ) -> tuple:
    """
    Get the active problems for a server database
    Args:
        serverID (int): The Discord server ID
    Returns:
        tuple: The row of the active problems
    """
    return dbh.getRow(dbt.ACTIVE_PROBLEMS.value, "serverID = ?", (serverID,))

def parseActiveProblems(row: tuple) -> dict:
    """
    Parse the Database row into a dictionary
    Args:
        row (tuple): The row from the database
    Returns:
        dict: The active problems as a dictionary. Contains:
            - p1 (str): The slug of the first problem
            - p2 (str): The slug of the second problem
            - p3 (str): The slug of the third problem
    """
    activeProblems = {
        "p1": row[1],
        "p2": row[2],
        "p3": row[3]
    }
    return activeProblems

def getAndParseActiveProblems(serverID: int) -> dict:
    """
    Get and parse the active problems for a server
    Args:
        serverID (int): The Discord server ID
    Returns:
        dict: The active problems as a dictionary. Contains:
            - p1 (str): The slug of the first problem
            - p2 (str): The slug of the second problem
            - p3 (str): The slug of the third problem
    """
    return parseActiveProblems(getActiveProblems(serverID))