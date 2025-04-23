import os
import random

from utils import file_helper as fh
from utils import logger

from core.problem import Problem, problemFromCSV
from core.problem_buckets import ProblemBucket
from core.server import Server, serverFromCSV

bucket = ProblemBucket()
servers: dict[int, Server] = dict()

# read from servers.csv to build servers
# use this to generate contests observers as we go
# read from problems.csv to build the problems then add to their appropriate server

DATAPATH = "data"

def generateRandomProblems(n) -> list[Problem]:
    lst = []
    for _ in range(n):
        pid = random.randint(1, 3)
        sid = random.randint(1, 10)
        difs = random.choice(["easy", "easy-medium", "medium-hard"])
        dow = random.randint(1, 7)
        hour = random.randint(0, 23)
        interval = random.randint(0, 3)
        temp = Problem(pid, sid, difs, dow, hour, interval)
        lst.append(temp)
    return lst

def generateTestServers() -> list[Server]:
    lst = []
    for i in range(1, 11):
        temp = Server(i, None)
        lst.append(temp)
    return lst

spath = os.path.join(DATAPATH, "servers.csv")
# servs = generateTestServers() # generate 10 servers with ids 1-10
# for serv in servs:
#     servers.add(serv)
#     fh.write_line_to_csv(spath, serv.toCSV())

read = fh.read_from_csv(spath)
for r in read:
    serv = serverFromCSV(r)
    servers[serv.serverID] = serv

ppath = os.path.join(DATAPATH, "problems.csv")
# problems = generateRandomProblems(50)
# for prob in problems:
#     line = prob.toCSV()
#     fh.write_line_to_csv(ppath, line)

read = fh.read_from_csv(ppath)
for r in read:
    prob = problemFromCSV(r)
    parent = servers[prob.serverID].addProblem(prob)
    bucket.addProblem(prob)

# bucket.printBucketClean()
print(servers)

for serverID in servers:
    server = servers[serverID]
    print(server.problems, end = "\n")
    print("------------------------------")