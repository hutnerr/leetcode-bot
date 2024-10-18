from tools import database_helper as dbh

from managers import problem_setting_manager as psm
from managers import problem_distrubutor as pmd
from managers import server_settings_manager as ssm

def getAllProblems(dow, hour):
    problems = problemsAtTheTime(dow, hour)
    return convertProblemRowToSendInfoList(problems)

def problemsAtTheTime(dow, hour):
    return dbh.getRowsWhere("problems", "dow = ? AND hour = ?", (dow, hour))

def convertProblemRowToSendInfoList(problems):
    problemsToSend = []
    
    for problem in problems:
        problemInfo = psm.parseProblemSettings(problem)
        key = f"{problemInfo['serverID']}-{problemInfo['problemNum']}"
        problemsToSend.append(key)
        
    return problemsToSend
