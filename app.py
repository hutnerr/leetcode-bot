from core.problem import Problem
from core.problem_buckets import ProblemBucket
from core.server import Server

bucket = ProblemBucket()
servers: set[Server] = set()

# read from servers.csv to build servers
# use this to generate contests observers as we go
# read from problems.csv to build the problems then add to their appropriate server
