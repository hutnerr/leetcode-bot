"""
This file contains functions that interact with the user settings database table.

Functions:
    - getUserSettings(userID: int) -> tuple
    - parseUserSettings(userRow: tuple) -> dict
    - getAndParseUserSettings(userID: int) -> dict
    - addPoints(userID: int, points: int) -> None
"""

from tools import database_helper as dbh
from tools.consts import DatabaseTables as dt

def getUserSettings(userID: int) -> tuple:
    """
    Gets the users settings from the database based on the Discord ID
    Args:
        userID (int): The Discord ID of the user
    Returns:
        tuple: The database row of the user settings
    """
    return dbh.getRow(dt.USER_SETTINGS.value, "userID = ?", (userID,))

def parseUserSettings(userRow: tuple) -> dict:
    """
    Converts the database row of the user settings into a dictionary
    Args:
        userRow (tuple): The database row of the user settings
    Returns:
        dict: The user settings in dictionary form. It has the keys:
            - userID (int): The Discord ID of the user
            - leetcodeUsername (str): The LeetCode username of the user
            - serverID (int): The Discord ID of the server the user is in
            - weeklyOpt (bool): The user's weekly problem option
            - biweeklyOpt (bool): The user's biweekly problem option
            - problemOpt (bool): The user's problem option
    """
    settings = {
        "userID": userRow[0],
        "leetcodeUsername": userRow[1],
        "serverID": userRow[2],
        "weeklyOpt": userRow[3],
        "biweeklyOpt": userRow[4],
        "problemOpt": userRow[5]
    }
    
    return settings

def getAndParseUserSettings(userID: int) -> dict:
    """
    Gets a database row of the users settings and convets it into a dictionary
    Args:
        userID (int): The Discord ID of the user
    Returns:
        dict: The user settings in dictionary form. It has the keys:
            - userID (int): The Discord ID of the user
            - leetcodeUsername (str): The LeetCode username of the user
            - serverID (int): The Discord ID of the server the user is in
            - weeklyOpt (bool): The user's weekly problem option
            - biweeklyOpt (bool): The user's biweekly problem option
            - problemOpt (bool): The user's problem option
    """
    return parseUserSettings(getUserSettings(userID))


def getUsernameFromID(userID: int) -> str:
    """
    Uses the Discord ID to get the LeetCode username of a user from a database 
    Args:
        userID (int): The discord ID of the user
    Returns:
        str: The LeetCode username of the user
    """
    return getAndParseUserSettings(userID)["leetcodeUsername"]


# TODO: Implement this function when I do the competition system
def addPoints(userID: int, points: int) -> None:
    pass