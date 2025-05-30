import os
import random
from pprint import pprint

from core.problem import Problem
from core.problem_buckets import ProblemBucket
from core.server import Server
from core.server_settings import ServerSettings

from utils import file_helper as fh
from utils import json_helper as jsonh

DATAPATH = "data"
spath = os.path.join(DATAPATH, "servers")

bucket = ProblemBucket()
servers: dict[int, Server] = dict()

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

def generateTestServers() -> list[Server]:
    lst = []
    for i in range(1, 11):
        temp_settings = ServerSettings(
            postingChannelID=random.randint(1000, 9999),
            weeklyContestAlerts=random.choice([True, False]),
            biweeklyContestAlerts=random.choice([True, False]),
            officialDailyAlerts=random.choice([True, False])
        )
        temp = Server(i, temp_settings)
        lst.append(temp)
    return lst

def generate():
    # generate the servers
    servs = generateTestServers() # generate 10 servers with ids 1-10
    for serv in servs:
        serv.toJSON() # this saves the server to JSON, creating a new file or overwriting the existing one
        servers[serv.serverID] = serv # add the server to the servers dict
    
    # generate the problems
    problems = generateRandomProblems(50)
    for prob in problems:
        sid = prob.serverID
        pid = prob.problemID
        
        server: Server = servers.get(sid)
        
        # if a problem exists within a server already, and we're going to update it,
        # we need to remove the old problem from the buckets first
        if server.problems[pid] is not None:
            old_problem = server.problems[pid]
            bucket.removeProblem(old_problem)
        
        # now we can add the new problem to the server
        if bucket.addProblem(prob):
            server.addProblem(prob) # add the problem to the server
        else:
            print("FAILED TO ADD PROBLEM TO BUCKET:", prob)
            server.removeProblem(prob)

        # might not need all these error checks and stuff
        if server is not None:
            if server.addProblem(prob): # add the problem to the server
                if not bucket.addProblem(prob):
                    print("FAILED TO ADD PROBLEM TO BUCKET:", prob)
                    server.removeProblem(prob)
            else:
                print("failed to add problem to server:", prob)
                bucket.removeProblem(prob)
                server.removeProblem(prob)

def readFromFiles():
    serverFiles = fh.getFilesInDirectory(spath) # get all server files in the directory
    for f in serverFiles:
        data = jsonh.readJSON(os.path.join(spath, f)) # read the JSON data using the file
        serv = Server.buildFromJSON(data) # build the server from JSON
        servers[serv.serverID] = serv # add the server to the servers dict

    for server in servers.values():
        for problem in server.problems:
            if problem is not None:
                if not bucket.addProblem(problem):
                    print("FAILED TO ADD PROBLEM TO BUCKET:", problem)

# ========================================================
# ========================================================
# ========================================================

def main():
    # generate()
    readFromFiles()
    
    # select one of the above to setup the structures
    # once theyre setup, we can test stuff
    
    tester = servers.get(1)  # get server with ID 1, assume it exists
    print(tester)
    

                
if __name__ == "__main__":
    main()