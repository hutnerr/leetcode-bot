from models.problem import Problem
from models.server import Server

# this bucket handles the times each individual problem is located at
# the bucket itself is a dict with dow as keys with values being a list of sets
# the list sets each pertain to a partciular hour and interval. 
# index can be calculated using _calculateBucketIndex(hour, interval)
class ProblemBucket:
    
    NUMINTERVALS = (60 // 15) # i want 15 min intervals, so 4 total
    NUMBUCKETS = (24 * NUMINTERVALS) # this is hours per day * num of 15 min intervals in hour

    def __init__(self):
        # dict with the days of week (1-7), then inside is a list of sets
        # use _calculateBucketIndex with the hour and interval for the right index
        self.buckets = {i: [set() for _ in range(self.NUMBUCKETS)] for i in range(1, 8)}

    def __str__(self) -> str:
        non_empty = [bucket for bucket in self.buckets if bucket]
        return str(non_empty)


    # ADDING AND REMOVING SHOULD BE CALLED BY A SYNCRONIZER
    # TO ENSURE THAT THE BUCKET AND MODEL CONTAIN THE SAME DATA
    def addToBucket(self, prob: Problem) -> bool:
        if (prob.problemID < 0) or (prob.problemID > Server.MAXPROBLEMS) or (prob.dow not in self.buckets):
            return False
        
        index = self._calculateBucketIndex(prob.hour, prob.interval)
        if index == -1:
            return False
        
        key = prob.getKey() # the key is the serverID::problemID, used later to trace back
        self.buckets[prob.dow][index].add(key)
        return True
    
    # ADDING AND REMOVING SHOULD BE CALLED BY A SYNCRONIZER
    # TO ENSURE THAT THE BUCKET AND MODEL CONTAIN THE SAME DATA
    def removeFromBucket(self, prob: Problem) -> bool:
        if prob.dow not in self.buckets:
            return False
        
        index = self._calculateBucketIndex(prob.hour, prob.interval)
        if index == -1:
            return False
        
        key = prob.getKey() # the key is the serverID::problemID, used later to trace back
        if key in self.buckets[prob.dow][index]:
            self.buckets[prob.dow][index].remove(key)
            return True
        return False
        

    def getBucket(self, dow: int, hour: int, interval: int) -> set | None:
        if dow not in self.buckets:
            return None
        
        index = self._calculateBucketIndex(hour, interval)
        if index == -1:
            return None
        
        return self.buckets[dow][index]
    
    
    # since the buckets for each day of weeks are lists, we can use a calculation
    # to determine the index for each hour and interval
    def _calculateBucketIndex(self, hour: int, interval: int) -> int:
        if (hour < 0 or hour > 24) or (interval < 0 or interval > self.NUMINTERVALS):
            return -1
        return (hour * self.NUMINTERVALS) + interval
    
    # FIXME: For testing, delete when product complete
    def printBucketClean(self) -> None:
        for day in self.buckets:
            print(f"===== DAY {day}=====")
            for i, bucket in enumerate(self.buckets[day]):
                if bucket:
                    hour = i // self.NUMINTERVALS
                    interval = i % self.NUMINTERVALS
                    print(f"[{hour:02d}:{interval * 15:02d}] -> {sorted(bucket)}")
