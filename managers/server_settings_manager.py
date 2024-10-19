"""
This module contains functions to get and parse server settings from the database.

Functions:
    - getAndParseServerSettings(serverID: int) -> dict
    - getServerSettings(serverID: int) -> tuple
    - parseServerSettings(serverRow: tuple) -> dict
    - getChannelToSendTo(serverID: int) -> int
    - optToggle(serverID: int, opt: str) -> None
    - getOptedUsers(serverID: int) -> dict
"""
from managers import user_setting_manager as usm

from tools import database_helper as dbh
from tools.consts import DatabaseTables as dbt
from tools.consts import DatabaseFields as dbf

def getAndParseServerSettings(serverID: int) -> dict:
    """
    Returns a dictionary of the server settings for the given serverID.
    Args:
        serverID (int): The serverID to get the settings for.
    Returns:
        dict: A dictionary containing the server settings. The dictionary has the following keys:
            - serverID (int): The unique ID for the server.
            - channelID (int): The ID of the channel to sent output.
            - problemsActive (int): How many problems are configured.
            - weeklyOpt (bool): Whether weekly contests alerts are enabled.
            - biweeklyOpt (bool): Whether biweekly contests alerts are enabled.
            - officialDaily (bool): Whether official daily contests alerts are enabled.
            - notifType (str): The type of notification to send.
            - timezone (str): The server's timezone (e.g., "UTC", "PST").
    """
    return parseServerSettings(getServerSettings(serverID))

def getServerSettings(serverID: int) -> tuple:
    """
    Performs a database search and returns the server settings for the given serverID
    Args:
        serverID (int): The serverID to get the settings for
    Returns:
        tuple: A tuple of the server settings
    """
    return dbh.getRow(dbt.SERVERS.value, "serverID = ?", (serverID,))

def parseServerSettings(serverRow: tuple) -> dict:
    """
    Converts the server settings tuple into a dictionary
    Args:
        serverRow (tuple): The tuple of server settings
    Returns:
        dict: A dictionary containing the server settings. The dictionary has the following keys:
            - serverID (int): The unique ID for the server.
            - channelID (int): The ID of the channel to sent output.
            - problemsActive (int): How many problems are configured.
            - weeklyOpt (bool): Whether weekly contests alerts are enabled.
            - biweeklyOpt (bool): Whether biweekly contests alerts are enabled.
            - officialDaily (bool): Whether official daily contests alerts are enabled.
            - notifType (str): The type of notification to send.
            - timezone (str): The server's timezone (e.g., "UTC", "PST").
    """
    serverSettings = {
        "serverID" : serverRow[0],
        "channelID" : serverRow[1],
        "problemsActive" : serverRow[2],
        "weeklyOpt" : serverRow[3],
        "biweeklyOpt" : serverRow[4],
        "officialDailyOpt" : serverRow[5],
        "notifType" : serverRow[6],
        "timezone" : serverRow[7]
    }
    return serverSettings

def getChannelToSendTo(serverID: int) -> int:
    """Getter for the output channel of this server
    Args:
        serverID (int): The server to get the output of
    Returns:
        int: The ID of the channel to send output to
    """
    serverRow = dbh.getRow(dbt.SERVERS.value, "serverID = ?", (serverID,))
    return parseServerSettings(serverRow)["channelID"]

def optToggle(serverID: int, opt: str) -> None:
    """
    The User ID to toggle the contest status
    Args:
        userID (int): The Discord Server ID 
        event (str): The event to toggle. Options are "weekly", "biweekly", "officialDaily"
    """
    column = ""
    if opt == "weekly":
        column = "weeklyOpt"
    elif opt == "biweekly":
        column = "biweeklyOpt"
    elif opt == "officialDaily":
        column = "officialDailyOpt"
    
    dbh.updateRow(dbt.USERS.value, column, not getAndParseServerSettings(serverID)[column], f"serverID = {serverID}")

# TODO: For the notification settings
def getOptedUsers(serverID: int) -> dict:
    """
    Gets a dict of the opted users for a server
    Args:
        serverID (int): The server ID to get the opted users for
    Returns:
        dict: The dict of the opted users. Has keys:
            - "problems" (list): The list of opted users for problems
            - "weekly" (list): The list of opted users for weekly contests
            - "biweekly" (list): The list of opted users for biweekly contests
            - "officialDaily" (list): The list of opted users for official daily contests
    """
    optedUsers = {
        "problems" : [],
        "weekly" : [],
        "biweekly" : [],
        "officialDaily" : []
    }
    
    usersInServer = dbh.getRowsWhere(dbt.USERS.value, "serverID = ?", (serverID,))
    
    for user in usersInServer:
        
        userSettings = usm.parseUserSettings(user)
        
        if userSettings["problemsOpt"]:
            optedUsers["problems"].append(userSettings["userID"])
            
        if userSettings["weeklyOpt"]:
            optedUsers["weekly"].append(userSettings["userID"])
            
        if userSettings["biweeklyOpt"]:
            optedUsers["biweekly"].append(userSettings["userID"])
            
        if userSettings["officialDailyOpt"]:
            optedUsers["officialDaily"].append(userSettings["userID"])
            
    return optedUsers

def addNewServer(serverID: int, channelID: int, timezone: str) -> bool:
    """
    Adds a new server to the database
    Args:
        serverID (int): The server ID
        channelID (int): The channel ID to send output to
        timezone (str): The timezone of the server
    Returns:
        bool: True if the server was added, False if not
    """
    if not serverExists(serverID):
        return dbh.addRow(dbt.SERVERS.value, dbf.SERVERS.value, (serverID, channelID, 0, 0, 0, 0, "simple", timezone))
    return False
        
def serverExists(serverID: int) -> bool:
    """
    Checks if a server exists in the database
    Args:
        serverID (int): The server ID
    Returns:
        bool: True if the server exists, False if not
    """
    return dbh.contains(dbt.SERVERS.value, "serverID = ?", (serverID,))
    
def updateServer(serverID: int, column: str, value: any) -> bool:
    """
    Updates the server in the database
    Args:
        serverID (int): The server ID
        channelID (int): The channel ID to send output to
        timezone (str): The timezone of the server
    Returns:
        bool: True if the server was added, False if not
    """
    if serverExists(serverID):
        return dbh.updateRow(dbt.SERVERS.value, column, value, f"serverID = {serverID}")
    return False
