import random

from models.problem import Problem
from models.server import Server
from models.user import User
from models.server_settings import ServerSettings

# generates problems with random parmeters
def generateRandomProblems(n) -> list[Problem]:
    lst = []
    for _ in range(n):
        pid = random.randint(1, Server.MAXPROBLEMS)  # problem IDs are 1-5
        sid = random.randint(1, 10)
        difs = random.choice(["easy", "medium", "hard", "easy-medium", "medium-hard", "easy-medium-hard", "hard-easy-medium"])
        dow = random.randint(1, 7) # 1-7, #FIXME: really should be 0-6 
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
            contestTimeIntervals=[random.choice([15, 30, 60, 120, 360, 720, 1440]) for _ in range(3)],  # 3 random intervals
            contestTimeAlerts=random.choice([True, False]),
            duplicatesAllowed=random.choice([True, False]),
            alertRoleID=random.randint(1000, 9999),
            useAlertRole=random.choice([True, False]),
        )
        previousProblems = ["two-sum"]
        temp = Server(i + 1, temp_settings, previousProblems)
        lst.append(temp)
    return lst

def generateTestUsers(n: int) -> dict[int, User]:
    users = dict()
    for i in range(0, n):
        user = User(
            discordID=random.randint(1000000000, 9999999999),
            leetcodeUsername=f"user{i}",
            points=random.randint(0, 1000)
        )
        users[user.discordID] = user
    return users

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

class GeneratedServers:
    def __init__(self):
        self.testServer1: Server = self.genServer1()
        self.testServer2: Server = self.genServer2()
        self.testServer3: Server = self.genServer3()
    
    def collectServers(self) -> dict[int, Server]:
        servers = {
            self.testServer1.serverID : self.testServer1,
            self.testServer2.serverID : self.testServer2,
            self.testServer3.serverID : self.testServer3,
        }
        return servers
    
    def genServer1(self) -> Server:
        serverSettings = ServerSettings(
            postingChannelID=12345,
            weeklyContestAlerts=True,
            biweeklyContestAlerts=True,
            officialDailyAlerts=True,
            contestTimeIntervals=[15, 30],
            contestTimeAlerts=True,
            duplicatesAllowed=True,
            alertRoleID=11111,
            useAlertRole=True
        )
        previousProblems = [
            "two-sum"
        ]
        server = Server(sid=1, settings=serverSettings, previousProblems=previousProblems)
        
        p1 = Problem(pid=1, sid=1, difs="easy-medium-hard", dow=1, hour=1, interval=1, premium=0)
        p2 = Problem(pid=2, sid=1, difs="easy-medium-hard", dow=1, hour=1, interval=1, premium=0)
        p3 = Problem(pid=3, sid=1, difs="easy-medium-hard", dow=1, hour=1, interval=1, premium=0)
        problems = [p1, p2, p3]
        
        for problem in problems:
            server.addProblem(problem)
        return server


    def genServer2(self) -> Server:
        serverSettings = ServerSettings(
            postingChannelID=12345,
            weeklyContestAlerts=False,
            biweeklyContestAlerts=False,
            officialDailyAlerts=False,
            contestTimeIntervals=[15, 30, 60, 120],
            contestTimeAlerts=False,
            duplicatesAllowed=False,
            alertRoleID=11111,
            useAlertRole=False
        )
        previousProblems = [
            "two-sum"
        ]
        server = Server(sid=2, settings=serverSettings, previousProblems=previousProblems)
        
        p1 = Problem(pid=1, sid=2, difs="easy", dow=1, hour=1, interval=0, premium=0)
        p2 = Problem(pid=2, sid=2, difs="medium", dow=2, hour=2, interval=0, premium=1)
        p3 = Problem(pid=3, sid=2, difs="hard", dow=3, hour=3, interval=0, premium=2)
        p4 = Problem(pid=4, sid=2, difs="easy-medium", dow=4, hour=4, interval=0, premium=0)
        p5 = Problem(pid=5, sid=2, difs="easy-medium-hard", dow=5, hour=5, interval=0, premium=0)
        problems = [p1, p2, p3, p4, p5]
        
        for problem in problems:
            server.addProblem(problem)
        return server
    
    def genServer3(self) -> Server:
        serverSettings = ServerSettings(
            postingChannelID=12345,
            weeklyContestAlerts=True,
            biweeklyContestAlerts=False,
            officialDailyAlerts=False,
            contestTimeIntervals=[],
            contestTimeAlerts=True,
            duplicatesAllowed=False,
            alertRoleID=11111,
            useAlertRole=False
        )
        previousProblems = [
            "two-sum"
        ]
        server = Server(sid=3, settings=serverSettings, previousProblems=previousProblems)
        
        p1 = Problem(pid=1, sid=3, difs="easy", dow=1, hour=1, interval=1, premium=0)
        p2 = Problem(pid=1, sid=3, difs="medium", dow=1, hour=1, interval=1, premium=0)
        p3 = Problem(pid=1, sid=3, difs="hard", dow=1, hour=1, interval=1, premium=0)
        p4 = Problem(pid=1, sid=3, difs="easy-medium", dow=1, hour=1, interval=1, premium=0)
        p5 = Problem(pid=1, sid=3, difs="easy-medium-hard", dow=1, hour=1, interval=1, premium=0)
        problems = [p1, p2, p3, p4, p5]
        
        for problem in problems:
            if not server.addProblem(problem):
                print(f"Failed to add problem {problem} to server {server.serverID}")
        return server
    
    