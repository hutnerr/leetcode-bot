""" 
Related to distributing problems to users

Functions: 
    - getProblem(file:str, dif:str) -> list
    - getProblemFromSettings(serverID: int, problemID: int) -> list
"""
import os

from tools import file_helper as fh
from tools import random_helper as rh
from tools.consts import Difficulty as difs

from managers import problem_setting_manager as psm

def getProblem(file:str, dif:str) -> list:
    """
    Get a problem from a problem set file based on the difficulty
    Args:
        file (str): The file name of the problem set. e.g "free.csv" or "paid.csv"
        dif (str): The csv difficulty string. e.g "Easy,Medium"
    Returns:
        list: The problem as a list of strings. e.g ["two-sum", "Easy", "false"]
    """
    problemsetFilepath = os.path.join("data", "problem_sets", file)
    problems = fh.fileToList(problemsetFilepath)
    difficulties = dif.split(",") 
    
    if len(difficulties) > 3 or len(difficulties) < 1:
        print("invalid difficulty string") 
        return None
    
    # we know we want a random problem if it was explicitly asked for or if all difficulties are allowed
    if dif == difs.RANDOM.value or len(difficulties) == 3:
        return rh.getRandom(problems).split(",")
    
    filtered = []
    
    # if there is only or two difficulties, we need to filter the problems to only those difficulties
    for problem in problems:
        if problem.split(",")[1] in difficulties:
            filtered.append(problem.split(","))

    return rh.getRandom(filtered)

def getProblemFromSettings(serverID: int, problemID: int) -> list:
    """
    Uses the settings of a problem to a problem that matches the requirements 
    Args:
        serverID (int): The Discord server ID
        problemID (int): The problem ID in the server
    Returns:
        list: The problem returned. Has the form ["slug", "difficulty", premium bool] 
    """
    problemInfo = psm.parseProblemSettings(psm.getProblem(serverID, problemID))
    problem = getProblem(str.lower(problemInfo["premium"]) + ".csv", problemInfo["difficulty"])
    return problem
    
