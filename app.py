import os
import random

from core.problem import Problem
from core.problem_buckets import ProblemBucket
from core.server import Server
from core.server_settings import ServerSettings

from utils import file_helper as fh
from utils import json_helper as jsonh

bucket = ProblemBucket()
servers: dict[int, Server] = dict()

# read from servers.csv to build servers
# use this to generate contests observers as we go
# read from problems.csv to build the problems then add to their appropriate server

DATAPATH = "data"

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
        temp_settings = ServerSettings() 
        temp = Server(i, temp_settings)
        lst.append(temp)
    return lst

# generate the testing servers 
# save them to JSON as we generate
spath = os.path.join(DATAPATH, "servers")
servs = generateTestServers() # generate 10 servers with ids 1-10
for serv in servs:
    serv.toJSON() # this will create a new server, and overwrite the existing one if it exists

# read the servers from the JSON files
serverFiles = fh.getFilesInDirectory(spath) # get all server files in the directory
for f in serverFiles:
    data = jsonh.readJSON(os.path.join(spath, f)) # read the JSON data using the file
    serv = Server.buildFromJSON(data) # build the server from JSON
    servers[serv.serverID] = serv # add the server to the servers dict

# generate random problems and add them to the servers
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

    if server is not None:
        if server.addProblem(prob): # add the problem to the server
            if not bucket.addProblem(prob):
                print("FAILED TO ADD PROBLEM TO BUCKET:", prob)
                server.removeProblem(prob)
        else:
            print("failed to add problem to server:", prob)
            bucket.removeProblem(prob)
            server.removeProblem(prob)

# we've generated new problems, time to update the servers and save them
# for server in servers.values():
#     server.toJSON()  # save the server to JSON

for server in servers.values():
    for problem in server.problems:
        if problem is not None:
            if not bucket.addProblem(problem):
                print("FAILED TO ADD PROBLEM TO BUCKET:", problem)

# at this point, our structures should be setup
# time to test the buckets 

# test the problems in bucket for 5:30
HOUR = 5
INTERVAL = 2

bucket.printBucketClean()

for problem in bucket.getProblems(HOUR, INTERVAL):
    serverid, problemid = map(int, problem.split("::"))
    print(f"{serverid} - {problemid} = ", end="")
    servers[serverid].handleProblem(problemid)

