from tools import database_helper as dbh
from managers import server_settings_manager as ssm
from tools.consts import Boundaries as bounds
from tools.consts import DatabaseFields as dbf



# ------------------------------
# Problem Counters
# ------------------------------

def getProblemCount(serverID):
    serverRow = dbh.getRow("servers", "serverID = ?", (serverID,))
    settings = ssm.parseServerSettings(serverRow)
    
    return settings['problems']

def increaseProblemCount(serverID) -> bool:
    problemCount = getProblemCount(serverID)
    
    if problemCount >= bounds.MAX_PROBLEMS.value:
        print("Error: Problem count is already at maximum")
        return False
    else:
        dbh.updateRow("servers", "problems", problemCount + 1, f"serverID = {serverID}")
        return True
    
def decreaseProblemCount(serverID) -> bool:
    problemCount = getProblemCount(serverID)
    
    if problemCount <= bounds.MIN_PROBLEMS.value:
        print("Error: Problem count is already at minimum")
        return False
    else:
        dbh.updateRow("servers", "problems", problemCount - 1, f"serverID = {serverID}")
        return True
        
# ------------------------------
# Adding, removing and updating
# ------------------------------
        
# problem table has:
# serverID, problemNum, dow, hour, difficulty, premium
        
def addProblem(serverID, problemID, dow, hour, difficulty, premium):
    if increaseProblemCount(serverID):
        dbh.addRow("problems", (dbf.PROBLEMS.value), (serverID, problemID, dow, hour, difficulty, premium))
        return True
    return False
        
def removeProblem(serverID, problemID):
    if dbh.contains("problems", "serverID = ? and problemNum = ?", (serverID, problemID)) and decreaseProblemCount(serverID):
        dbh.removeRow("problems", "serverID = ? AND problemNum = ?", (serverID, problemID))
        return True
    return False
        
def updateProblem(serverID, problemID, column, value):
    if dbh.contains("problems", "serverID = ? and problemNum = ?", (serverID, problemID)):
        dbh.updateRow("problems", column, value, f"serverID = {serverID} AND problemNum = {problemID}")
        return True
    return False
# ------------------------------
# get problems for a server
# ------------------------------

def getProblem(serverID, problemID):
    return dbh.getRow("problems", "serverID = ? AND problemNum = ?", (serverID, problemID))

def getProblems(serverID):
    return dbh.getRows("problems", "serverID = ?", (serverID,))

def parseProblemSettings(problemRow:tuple) -> dict:
    settings = {
        "serverID" : problemRow[0],
        "problemNum" : problemRow[1],
        "dow" : problemRow[2],
        "hour" : problemRow[3],
        "difficulty" : problemRow[4],
        "premium" : problemRow[5]
    }
    return settings