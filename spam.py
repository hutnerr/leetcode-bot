import os
import random

from core.buckets.dow_buckets import DowBucket
from core.buckets.static_buckets import StaticBucket
from core.buckets.contest_alert_buckets import ContestAlertBucket

from core.managers.cache_manager import CacheManager
from core.managers.problem_manager import ProblemManager
from core.managers.query_manager import QueryManager, Query

from core.problem import Problem
from core.server import Server
from core.server_settings import ServerSettings

from utils import file_helper as fh
from utils import json_helper as jsonh

# =========================================================
# ================== Gen/Build Servers ====================
# =========================================================

def generateRandomProblems(n) -> list[Problem]:
    lst = []
    for _ in range(n):
        pid = random.randint(1, Server.MAXPROBLEMS)  # problem IDs are 1-5
        sid = random.randint(1, 10)
        difs = random.choice(["easy", "medium", "hard", "easy-medium", "medium-hard", "easy-medium-hard", "hard-easy-medium"])
        dow = random.randint(1, 7) # 1-7
        hour = random.randint(0, 10) # 0-23
        interval = random.randint(0, 2) # 0-3
        premium = random.randint(0, 2) # 0=free, 1=premium, 2=either
        temp = Problem(pid, sid, difs, dow, hour, interval, premium)
        lst.append(temp)
    return lst

def generateTestServers(n = 11) -> list[Server]:
    lst = []
    for i in range(1, n):
        temp_settings = ServerSettings(
            postingChannelID=random.randint(1000, 9999),
            weeklyContestAlerts=random.choice([True, False]),
            biweeklyContestAlerts=random.choice([True, False]),
            officialDailyAlerts=random.choice([True, False]),
            contestAlertIntervals=[random.choice([15, 30, 60, 120, 360, 720, 1440]) for _ in range(3)]  # 3 random intervals
        )
        temp = Server(i, temp_settings)
        lst.append(temp)
    return lst

def generate():
    # generate the servers
    servers: dict[int, Server] = dict()
    servs = generateTestServers() # generate 10 servers with ids 1-10
    for serv in servs:
        serv.toJSON()
        servers[serv.serverID] = serv # add the server to the servers dict
    
    # generate the problems
    problems = generateRandomProblems(50)
    for prob in problems:        
        server: Server = servers.get(prob.serverID)
        server.addProblem(prob)
    return servers

def readFromFiles():
    # problems are saved within the servers json file so they're read in
    # when the server is built from JSON
    spath = os.path.join("data", "servers")
    servers: dict[int, Server] = dict()
    serverFiles = fh.getFilesInDirectory(spath)
    for f in serverFiles:
        data = jsonh.readJSON(os.path.join(spath, f))
        serv = Server.buildFromJSON(data)
        servers[serv.serverID] = serv
    return servers

# ========================================================
# ================== Setup Buckets =======================
# ========================================================

def setupBuckets(servers):
    dowBucket = DowBucket()
    staticBucket = StaticBucket()
    contestAlertBucket = ContestAlertBucket()

    # the dowBucket has a ProblemBucket object for each day of the week
    def addServerToDowProblemBucket(server: Server):
        for problem in server.problems:
            if problem is not None:
                if not dowBucket.addToBucket(problem):
                    print("Failed to add problem to bucket:", problem)

    def addServerToStaticBucket(server: Server):
        settings = server.settings
        if settings.weeklyContestAlerts:
            staticBucket.addToWeeklyBucket(server.serverID)
            
        if settings.biweeklyContestAlerts:
            staticBucket.addToBiweeklyBucket(server.serverID)
            
        if settings.officialDailyAlerts:
            staticBucket.addToDailyBucket(server.serverID)

    def addServerToContestAlertBucket(server: Server):
        settings = server.settings
        for interval in settings.contestAlertIntervals:
            contestAlertBucket.addToBucket(interval, server.serverID)

    for server in servers.values():
        addServerToDowProblemBucket(server)
        addServerToStaticBucket(server)
        addServerToContestAlertBucket(server)

    return (dowBucket, staticBucket, contestAlertBucket)

# ========================================================
# ================== Setup Managers =======================
# ========================================================

def setupCacheManager():
    return CacheManager()

def setupQueryManager():
    return QueryManager()

def setupProblemManager(servers, dowBucket):
    return ProblemManager(servers, dowBucket)

def setupManagers(servers, dowBucket):
    cacheManager = setupCacheManager()
    queryManager = setupQueryManager()
    problemManager = setupProblemManager(servers, dowBucket)
    return (cacheManager, queryManager, problemManager)

# ========================================================
# ==================== Setup App =========================
# ========================================================

def main():
    # servers = generate()
    servers = readFromFiles()
    dowBucket, staticBucket, contestAlertBucket = setupBuckets(servers)
    cacheManager, queryManager, problemManager = setupManagers(servers, dowBucket)
    
    
    for problem in generateRandomProblems(100000):
        problemManager.selectProblem(problem)
    
    # problem = generateRandomProblems(1)[0]
    # problemSlug = problemManager.selectProblem(problem)
    # problemSlug = "two-sum"

    # if cacheManager.existsInCache(problemSlug):
    #     print("Getting from cache")
    #     problemInfo = cacheManager.getFromCache(problemSlug)
    # else:
    #     print("Performing query")
    #     problemInfo = queryManager.performQuery(Query.QUESTION_INFO, {"titleSlug" : problemSlug})
    #     cacheManager.cacheProblem(problemInfo)
    
    # print(problemInfo)
    
    

def testIfBucketHasOldProblemsWhenAdding():
    DOW = 1
    SERVERID = 1
    PROBLEMID =1 
    
    server = generateTestServers(2)[0] # 2 because range is 1,n and n is not inclusive so it gens 1    
    server.serverID = SERVERID
    server.toJSON()        
    
    servers: dict[int, Server] = dict()
    servers[server.serverID] = server # add the server to the servers dict
    
    dowBucket = DowBucket()
    problemManager = setupProblemManager(servers, dowBucket)
    
    problems = generateRandomProblems(3)
    for problem in problems:
        problem.dow = DOW
        problem.problemID = PROBLEMID
        problem.serverID = SERVERID

    p1, p2, p3 = problems
    
    x1 = problemManager.addProblem(p1)
    x2 = problemManager.addProblem(p2)
    x3 = problemManager.addProblem(p3)    
    print(x1, x2, x3)
    
    print(server)
    dowBucket.getBucket(DOW).printBucketClean()

    problemManager.removeProblem(p3)
    print("After removing p1:")
    print(server)
    dowBucket.getBucket(DOW).printBucketClean()

if __name__ == "__main__":
    main()
    # testIfBucketHasOldProblemsWhenAdding()