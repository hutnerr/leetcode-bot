"""
Manager for working with and retrieving contest times

Functions:
    - getContestInfo() -> dict
    - parseContestsInfo(contestsInfo: dict) -> dict
    - getAndParseContestsInfo() -> dict
    - getServersForContestTime(timeColumn: str) -> list
"""
from tools import database_helper as dbh
from tools import query_helper as qh
from tools import time_helper as th
from tools.consts import Query as q
from tools.consts import DatabaseTables as dbt
from tools.consts import Times as t

def getContestsInfo() -> dict:
    """
    Perform a query to get the upcoming contests times
    Returns:
        dict: The json response from the query
    """
    return qh.performQuery(q.UPCOMING_CONTESTS.value, {})

def parseContestsInfo(contestsInfo: dict) -> dict:
    """
    Convert the json response from the query into a dictionary
    Args:
        contestsInfo (dict): The json response from the query
    Returns:
        dict: A dict with the contest titles and times. Contains:
            - weekly: (str, str) - The title and time away of the weekly contest
            - biweekly: (str, str) - The title and time away of the biweekly contest
    """
    base = contestsInfo['data']['upcomingContests']
    
    weeklyTime = th.distanceAway(th.fromTimestamp(base[0]["startTime"]))
    biweeklyTime = th.distanceAway(th.fromTimestamp(base[1]["startTime"]))
    
    contestDict = {
        "weekly" : (base[0]["title"], weeklyTime),
        "biweekly" : (base[1]["title"], biweeklyTime),
    }
    return contestDict

def getAndParseContestsInfo() -> dict:
    """
    Gets and parses the contests info into a dict
    Returns:
        dict: A dict with the contest titles and times. Contains:
            - weekly: (str, str) - The title and time away of the weekly contest
            - biweekly: (str, str) - The title and time away of the biweekly contest    
    """
    contestsInfo = getContestsInfo()
    return parseContestsInfo(contestsInfo)

def getServersForContestTime(timeColumn: str) -> list:
    """
    The servers that want alerts for the specified time
    Args:
        timeColumn (str): The time we're looking for. e.g. The values in the Contest database
    \nThe values should be from the constants in tools.consts.Times

    Returns:
        list: The servers that want alerts for the specified time
    """
    validTimes = t.CONTEST_TIME_ALERTS.value
    
    if timeColumn not in validTimes:
        print(f"Invalid timeColumn: {timeColumn}")
        return []
    
    serverRows = dbh.getRowsWhere(dbt.CONTESTS.value, f"{timeColumn} = ?", 1) # 1 means true
    
    serverIDList = []
    
    for server in serverRows:
        serverIDList.append(server[0])
    
    pass