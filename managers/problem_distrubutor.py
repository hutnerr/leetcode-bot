import os

from tools import file_helper as fh
from tools import random_helper as rh
from tools import database_helper as dbh

from tools.consts import Difficulty as difs
from tools.consts import Premium as prem
from tools.consts import Problemset as ps
from tools.consts import DatabaseTables as dbt
from tools.consts import DatabaseFields as dbf

from managers import problem_setting_manager as psm

def getProblem(file:str, dif:str) -> list:
    
    problemsetFilepath = os.path.join("data", "problem_sets", file)
    problems = fh.fileToList(problemsetFilepath)
    
    # list will be [1, 2, 3] for easy, medium, hard
    # difs is a csv string of the allowed difficulties
    difficulties = dif.split(",") 
    
    if len(difficulties) > 3:
        print("invalid difficulty string") 
        return None
    
    # we know we want a random problem if it was explicitly asked for or if all difficulties are allowed
    if int(dif) == difs.RANDOM.value or len(difficulties) == 3:
        return rh.getRandom(problems).split(",")
    
    # if there is only or two difficulties, we need to filter the problems to only those difficulties
    if len(difficulties) == 1:
        filtered = [problem.split(",") for problem in problems if problem.split(",")[1] == difficulties[0]]
    elif len(difficulties) == 2:
        filtered = [problem.split(",") for problem in problems if problem.split(",")[1] == difficulties[0] or problem.split(",")[1] == difficulties[1]]

    # now that we've filtered, we can make our random choice 
    return rh.getRandom(filtered)

def determineProblemset(premium:int) -> str:
    if premium == prem.FREE.value:
        return ps.FREE.value
    elif premium == prem.PAID.value:
        return ps.PAID.value
    else:
        return ps.BOTH.value

def getProblemsFromSettings(serverID, problemID):
    problemInfo = psm.parseProblemSettings(psm.getProblem(serverID, problemID))
    problem = getProblem(determineProblemset(int(problemInfo["premium"])), problemInfo["difficulty"])
    return problem
    
