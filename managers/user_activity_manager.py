

from tools import query_helper as qh
from tools.consts import Query as q
from tools import database_helper as dbh

from managers import user_setting_manager as usm

# Check the users most recent activity, see if the problem 
def getRecentProblemsSolved(username:str, amount:int = 5) -> list:
    result = qh.performQuery(q.RECENT_SUBMISSIONS.value, {"username": username, "limit": amount})
    result = result["data"]["recentAcSubmissionList"]
    for i in range(len(result)):
        result[i] = result[i]["titleSlug"]
        
    return result

def getUsernameFromID(userID:int):
    userRow = dbh.getRow("users", "userID = ?", (userID,))
    return usm.parseUserSettings(userRow)["leetcodeUsername"]

def checkIfRecentlySolved(userID:str, problemSlug:str) -> bool:
    username = getUsernameFromID(userID)
    problems = getRecentProblemsSolved(username)
    return problemSlug in problems
    
    