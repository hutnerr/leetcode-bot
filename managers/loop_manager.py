"""
Functions related to the continuous loop that the discord bot runs

Functions:
    - getAllProblems(dow: str, hour: int) -> list
    - problemsAtTheTime(dow: str, hour: int) -> tuple
    - convertProblemRowToSendInfoList(problems: tuple) -> list
"""
from tools import database_helper as dbh

from managers import problem_setting_manager as psm

def getAllProblems(dow: str, hour: int) -> list:
    """
    Get all problems that fit the given day and hour
    Args:
        dow (str): The day of the week. e.g. "Monday" or "Friday"
        hour (int): The hour of the day in 24 hour time. e.g. 0 - 23
    Returns:
        list: Problems that fit the given day and hour
    """
    problems = problemsAtTheTime(dow, hour)
    return convertProblemRowToSendInfoList(problems)

def problemsAtTheTime(dow: str, hour: int) -> tuple:
    """
    Returns all problems that are scheduled for the given day and hour
    Args:
        dow (str): The day of the week e.g. "Monday"
        hour (int): The hour we're looking for. e.g. 0 - 23
    Returns:
        tuple: The rows that are schedules
    """
    return dbh.getRowsWhere("problems", "dow LIKE ?", (f"%{dow}%", hour))

def convertProblemRowToSendInfoList(problems: tuple) -> list:
    """
    Convert a tuple of problem rows to a list of keys in the form serverID-problemNum so we can search for it in the problems table
    Args:
        problems (tuple): The rows we want to convert
    Returns:
        list: The keys of the problems
    """
    problemsToSend = []
    
    for problem in problems:
        problemInfo = psm.parseProblemSettings(problem)
        key = f"{problemInfo['serverID']}-{problemInfo['problemNum']}"
        problemsToSend.append(key)
        
    return problemsToSend
