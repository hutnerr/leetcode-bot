import random

from core.models.problem import Problem
from core.models.server import Server
from core.models.server_settings import ServerSettings

# generates problems with random parmeters
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

# generates test servers
def generateTestServers(n: int) -> list[Server]:
    lst = []
    for i in range(0, n):
        temp_settings = ServerSettings(
            postingChannelID=random.randint(1000, 9999),
            weeklyContestAlerts=random.choice([True, False]),
            biweeklyContestAlerts=random.choice([True, False]),
            officialDailyAlerts=random.choice([True, False]),
            contestAlertIntervals=[random.choice([15, 30, 60, 120, 360, 720, 1440]) for _ in range(3)],  # 3 random intervals
            duplicatesAllowed=random.choice([True, False]),
            alertRoleID=random.randint(1000, 9999),
            useAlertRole=random.choice([True, False]),
        )
        previousProblems = ["two-sum"]
        temp = Server(i + 1, temp_settings, previousProblems)
        lst.append(temp)
    return lst

# generates servers, then generates problems and adds them to the servers
def generate(nservers = 10, nproblems = 50):
    # generate the servers
    servers: dict[int, Server] = dict()
    servs = generateTestServers(nservers) # generate 10 servers with ids 1-10
    for serv in servs:
        serv.toJSON()
        servers[serv.serverID] = serv # add the server to the servers dict
    
    # generate the problems
    problems = generateRandomProblems(nproblems)
    for prob in problems:        
        server: Server = servers.get(prob.serverID)
        server.addProblem(prob)
    return servers
