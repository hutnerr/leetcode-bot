from tools import query_helper as qh
from tools.consts import Query as q
from tools import time_helper as th

def getContestsInfo():
    return qh.performQuery(q.UPCOMING_CONTESTS.value, {})

def parseContestsInfo(contestsInfo):
    base = contestsInfo['data']['upcomingContests']
    
    weeklyTime = th.distanceAway(th.fromTimestamp(base[0]["startTime"]))
    biweeklyTime = th.distanceAway(th.fromTimestamp(base[1]["startTime"]))
    
    contestDict = {
        "weekly" : (base[0]["title"], weeklyTime),
        "biweekly" : (base[1]["title"], biweeklyTime),
    }
    
    return contestDict

def getAndParseContestsInfo():
    contestsInfo = getContestsInfo()
    return parseContestsInfo(contestsInfo)