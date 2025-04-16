from core.problem import Problem
from core.problem_buckets import ProblemBucket
from core.server import Server

bucket = ProblemBucket()
servers: set[Server] = set()

# Helper to add many problems per server
def add_many_problems(server: Server, base_hour: int, base_id: int):
    difficulties = ['easy', 'medium', 'hard']
    count = 0
    for i in range(5):  # 5 problems per server
        hour = base_hour + (i % 3)  # wraps over 3 hours
        interval = i % 4  # 0-3 (15 min intervals)
        dif = difficulties[i % len(difficulties)]
        prob = Problem(
            pid=base_id + i,
            sid=server.serverID,
            difs=dif,
            dow=(i % 7) + 1,
            hour=hour,
            interval=interval
        )
        server.addProblem(prob)
        bucket.addProblem(prob)
        count += 1
    print(f"Added {count} problems for server {server.serverID}.")

# Print function for a given bucket
def print_bucket(hour: int, interval: int):
    problems = bucket.getProblems(hour, interval)
    print(f"\n--- Bucket for {hour}:{interval * 15:02} ---")
    if problems:
        for p in problems:
            print(p)
    else:
        print("No problems.")

# Setup servers
server1 = Server(1111)
server2 = Server(2222)
server3 = Server(3333)

servers.update([server1, server2, server3])

add_many_problems(server1, base_hour=8, base_id=0)
add_many_problems(server2, base_hour=9, base_id=100)
add_many_problems(server3, base_hour=10, base_id=200)

# Print some shared buckets to show overlapping
print_bucket(9, 0)   # May include problems from multiple servers
print_bucket(10, 1)
print_bucket(11, 2)
print_bucket(12, 3)

# Optional: print all server problems
for server in servers:
    print(f"\n--- Problems for Server {server.serverID} ---")
    for prob in server.problems:
        if prob:
            print(prob)
