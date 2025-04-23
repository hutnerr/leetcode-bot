from core.problem import Problem
from core.server import Server

class ProblemBucket:
    
    NUMINTERVALS = (60 // 15) # i want 15 min intervals, so 4 total
    NUMBUCKETS = (24 * NUMINTERVALS) # this is hours per day * num of 15 min intervals in hour

    def __init__(self):
        self.buckets = [set() for _ in range(self.NUMBUCKETS)]
        
    def getBucket(self, hour: int, interval: int) -> int:
        if (hour < 0 or hour > 24) or (interval < 0 or interval > self.NUMINTERVALS):
            return -1
        return (hour * self.NUMINTERVALS) + interval
    
    # gets the problems in this bucket
    def getProblems(self, hour: int, interval: int) -> set | None:
        bucket = self.getBucket(hour, interval)
        if bucket == -1:
            return None
        return self.buckets[bucket]
    
    def addProblem(self, prob: Problem) -> bool:
        bucket = self.getBucket(prob.hour, prob.interval)
        if bucket == -1:
            return False
        if prob.problemID < 0 or prob.problemID >= Server.MAXPROBLEMS:
            return False
        key = prob.getKey()
        self.buckets[bucket].add(key)
        return True
    
    def getEntireBucket(self) -> list[dict]:
        return self.buckets
    
    def printBucketClean(self) -> None:
        for i, bucket in enumerate(self.buckets):
            if bucket:
                hour = i // self.NUMINTERVALS
                interval = i % self.NUMINTERVALS
                print(f"[{hour:02d}:{interval * 15:02d}] -> {sorted(bucket)}")
