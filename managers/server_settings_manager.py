"""
This module contains functions to get and parse server settings from the database.

Functions:
    - getAndParseServerSettings(serverID: int) -> dict
    - getServerSettings(serverID: int) -> tuple
    - parseServerSettings(serverRow: tuple) -> dict
    - getChannelToSendTo(serverID: int) -> int
"""

from tools import database_helper as dbh
from tools.consts import DatabaseTables as dbt

def getAndParseServerSettings(serverID: int) -> dict:
    """
    Returns a dictionary of the server settings for the given serverID.
    Args:
        serverID (int): The serverID to get the settings for.
    Returns:
        dict: A dictionary containing the server settings. The dictionary has the following keys:
            - id (int): The unique ID for the server.
            - channelID (int): The ID of the channel to sent output.
            - problems (int): How many problems are configured.
            - weeklyContests (bool): Whether weekly contests alerts are enabled.
            - biweeklyContests (bool): Whether biweekly contests alerts are enabled.
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
            - id (int): The unique ID for the server.
            - channelID (int): The ID of the channel to sent output.
            - problems (int): How many problems are configured.
            - weeklyContests (bool): Whether weekly contests alerts are enabled.
            - biweeklyContests (bool): Whether biweekly contests alerts are enabled.
            - timezone (str): The server's timezone (e.g., "UTC", "PST").
    """
    serverSettings = {
        "id" : serverRow[0],
        "channelID" : serverRow[1],
        "problems" : serverRow[2],
        "weeklyContests" : serverRow[3],
        "biweeklyContests" : serverRow[4],
        "timezone" : serverRow[5]
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
