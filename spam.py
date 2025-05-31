import os
import random

from core.buckets.dow_buckets import DowBucket
from core.buckets.static_buckets import StaticBucket
from core.buckets.contest_alert_buckets import ContestAlertBucket

from core.managers.cache_manager import CacheManager
from core.managers.problem_manager import ProblemManager
from core.managers.query_manager import QueryManager

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
        difs = random.choice(["easy", "easy-medium", "medium-hard"])
        dow = random.randint(1, 7) # 1-7
        hour = random.randint(0, 10) # 0-23
        interval = random.randint(0, 2) # 0-3
        temp = Problem(pid, sid, difs, dow, hour, interval)
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
    return 

def setupQueryManager():
    pass

def setupProblemManager(dowBucket):
    pass

def setupManagers(dowBucket):
    pass

# ========================================================
# ==================== Setup App =========================
# ========================================================

def main():
    # servers = generate()
    servers = readFromFiles()
    
    dowBucket, staticBucket, contestAlertBucket = setupBuckets(servers)
    
    


def testIfBucketHasOldProblemsWhenAdding():
    DOW = 1
    SERVERID = 1
    PROBLEMID =1 
    
    dowBucket = DowBucket()        
    server = generateTestServers(2)[0]
    server.serverID = SERVERID
    
    problems = generateRandomProblems(3)
    for problem in problems:
        problem.dow = DOW
        problem.problemID = PROBLEMID
        problem.serverID = SERVERID

    p1, p2, p3 = problems
    
    # after the subsequent calls below, the server and the bucket should both only have 1 problem in them
    server.addProblem(p1)
    dowBucket.addToBucket(p1)
    
    server.addProblem(p2)
    dowBucket.addToBucket(p2)
    
    server.addProblem(p3)
    dowBucket.addToBucket(p3)
    
    print(server)
    dowBucket.getBucket(DOW).printBucketClean()


if __name__ == "__main__":
    # main()
    testIfBucketHasOldProblemsWhenAdding()