import os
import random

from utils import file_helper as fh
from utils import logger

from core.problem import Problem, problemFromCSV
from core.problem_buckets import ProblemBucket
from core.server import Server

bucket = ProblemBucket()
servers: set[Server] = set()

# read from servers.csv to build servers
# use this to generate contests observers as we go
# read from problems.csv to build the problems then add to their appropriate server

DATAPATH = "data"

def generateRandomProblems(n) -> list[Problem]:
    lst = []
    for i in range(n):
        pid = random.randint(1, 3)
        sid = random.randint(1, 100)
        difs = random.choice(["easy", "easy-medium", "medium-hard"])
        dow = random.randint(1, 7)
        hour = random.randint(0, 23)
        interval = random.randint(0, 3)
        temp = Problem(pid, sid, difs, dow, hour, interval)
        lst.append(temp)
    
    return lst

path = os.path.join(DATAPATH, "problems.csv")

# problems = generateRandomProblems(50)

# for prob in problems:
#     line = prob.toCSV()
#     fh.write_line_to_csv(path, line)

read = fh.read_from_csv(path)
for r in read:
    prob = problemFromCSV(r)
    bucket.addProblem(prob)
    
bucket.printBucketClean()