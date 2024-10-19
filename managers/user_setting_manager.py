"""
This file contains functions that interact with the user settings database 

Functions:
    - getUserSettings(userID: int) -> tuple
    - parseUserSettings(userRow: tuple) -> dict
    - getAndParseUserSettings(userID: int) -> dict
    - addPoints(userID: int, points: int) -> None
    - getRecentProblemsSolved(username: str, amount: int = 5) -> list
    - checkIfRecentlySolved(userID: int, problemSlug: str) -> bool
"""
from managers import user_setting_manager as usm 

from tools import query_helper as qh
from tools import database_helper as dbh
from tools.consts import DatabaseTables as dbt
from tools.consts import DatabaseFields as dbf
from tools.consts import Query as q

def getUserSettings(userID: int) -> tuple:
    """
    Gets the users settings from the database based on the Discord ID
    Args:
        userID (int): The Discord ID of the user
    Returns:
        tuple: The database row of the user settings
    """
    return dbh.getRow(dbt.USERS.value, "userID = ?", (userID,))

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
            - officialDailyOpt (bool): The user's official daily problem option
    """
    settings = {
        "userID": userRow[0],
        "leetcodeUsername": userRow[1],
        "serverID": userRow[2],
        "weeklyOpt": userRow[3],
        "biweeklyOpt": userRow[4],
        "problemsOpt": userRow[5],
        "officialDailyOpt": userRow[6]
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
            - officialDailyOpt (bool): The user's official daily problem option
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

# TODO: For the Notifcation System
def optToggle(userID: int, event: str) -> None:
    """
    The User ID to toggle the contest status
    Args:
        userID (int): The Discord ID of the user
        event (str): The event to toggle. Options are "weekly", "biweekly", "problem"
    """
    column = ""
    if event == "weekly":
        column = "weeklyOpt"
    elif event == "biweekly":
        column = "biweeklyOpt"
    elif event == "problem":
        column = "problemsOpt"
    elif event == "officialDaily":
        column = "officialDailyOpt"
    
    dbh.updateRow(dbt.USERS.value, column, not getAndParseUserSettings(userID)[column], f"userID = {userID}")


def addNewUser(userID: int, leetcodeUsername: str, serverID: int) -> None:
    """
    Adds a new user to the database
    Args:
        userID (int): The Discord ID of the user
        leetcodeUsername (str): The LeetCode username of the user
        serverID (int): The Discord ID of the server the user is in
    """
    if not userExists(userID):
        # Default state is only opted into server problems, not contests 
        dbh.addRow(dbt.USERS.value, dbf.USERS.value, (userID, leetcodeUsername, serverID, False, False, True))
    else:
        print("User already exists")

def removeUser(userID: int) -> None:
    """
    Removes a user from the database
    Args:
        userID (int): The Discord ID of the user
    """
    if userExists(userID):
        dbh.removeRow(dbt.USERS.value, "userID = ?", (userID,))
    else:
        print("User does not exist")

def changeLeetcodeUsername(userID: int, leetcodeUsername: str) -> None:
    """
    Updates the users LeetCode username 
    Args:
        userID (int): The Discord ID of the user
        leetcodeUsername (str): The new LeetCode username of the user
    """
    if userExists(userID):
        dbh.updateRow(dbt.USERS.value, "leetcodeUsername", leetcodeUsername, f"userID = {userID}")
    else:
        print("User does not exist")

def userExists(userID: int) -> bool:
    """
    Checks if a user exists in the database
    Args:
        userID (int): The Discord ID of the user
    Returns:
        bool: True if the user exists, False if the user does not exist
    """
    return getUserSettings(userID) is not None

def getRecentProblemsSolved(username: str, amount: int = 5) -> list:
    """ 
    Get the most recent problems solved by a user
    
    Args:
        username (str): The LeetCode username of the user
        amount (int): The amount of problems to get. If not specified, it will default to 5
    Returns:
        list: A list of the `amount` recent problems solved by the user    
    """
    result = qh.performQuery(q.RECENT_SUBMISSIONS.value, {"username": username, "limit": amount})
    result = result["data"]["recentAcSubmissionList"] # trim the query result
    for i in range(len(result)):
        result[i] = result[i]["titleSlug"] # only keep the slug
    return result

def checkIfRecentlySolved(userID: int, problemSlug: str) -> bool:
    """
    Performs a query to check if a user has solved a problem recently
    Args:
        userID (int): The discord ID of the user
        problemSlug (str): The slug of the problem to check 
    Returns:
        bool: True if the user has solved the problem recently, False otherwise
    """
    username = usm.getUsernameFromID(userID)
    problems = getRecentProblemsSolved(username)
    return problemSlug in problems

# TODO: Implement this function when I do the competition system
def addPoints(userID: int, points: int) -> None:
    pass