# stores a problem bucket for each day of the week
from core.buckets.problem_buckets import ProblemBucket
from core.problem import Problem
from core.server import Server

class DowBucket:
    def __init__(self):
        self.buckets: dict[int, ProblemBucket] = {i: ProblemBucket() for i in range(8)}  # 1-7 for Sunday-Saturday, 0 is unused
        
    def __str__(self) -> str:
        return str(self.buckets)

    def printBucketClean(self):
        print("Day of Week Buckets:")
        for day, bucket in self.buckets.items():
            print(f"  Day {day}: {bucket}")

    def addToBucket(self, problem: Problem) -> bool:
        day = problem.dow
        if day in self.buckets:
            return self.buckets[day].addProblem(problem)
        return False

    def removeFromBucket(self, day: int, serverID: int):
        if day in self.buckets:
            self.buckets[day].removeProblem(serverID)

    def getBucket(self, day: int) -> ProblemBucket:
        return self.buckets.get(day, ProblemBucket())
    
    def notifyServers(self, servers:dict[int, Server], dow: int, hour: int, interval: int):
        self.buckets[dow].notifyServers(servers, hour, interval)
        
