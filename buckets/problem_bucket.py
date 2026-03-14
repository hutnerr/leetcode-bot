from models.problem import Problem
from models.server import Server
from pyutils import Clogger

# this bucket handles the times each individual problem is located at
# the bucket itself is a dict with dow as keys with values being a list of sets
# the list sets each pertain to a partciular hour and interval. 
# index can be calculated using _calculateBucketIndex(hour, interval)
class ProblemBucket:
    
    NUMINTERVALS = (60 // 15) # i want 15 min intervals, so 4 total
    NUMBUCKETS = (24 * NUMINTERVALS) # this is hours per day * num of 15 min intervals in hour

    def __init__(self):
        # dict with the days of week (0-6), then inside is a list of sets
        # use _calculateBucketIndex with the hour and interval for the right index
        # sunday is 0, monday is 1, etc. saturday is 6
        self.buckets = {i: [set() for _ in range(self.NUMBUCKETS)] for i in range(0, 7)}
        Clogger.info("Initialized ProblemBucket.")

    def __str__(self) -> str:
        non_empty = [bucket for bucket in self.buckets if bucket]
        return str(non_empty)


    # ADDING AND REMOVING SHOULD BE CALLED BY A SYNCRONIZER
    # TO ENSURE THAT THE BUCKET AND MODEL CONTAIN THE SAME DATA
    def addToBucket(self, prob: Problem) -> bool:
        if (prob.problemID < 0) or (prob.problemID > Server.MAXPROBLEMS) or (not prob.dows):
            Clogger.warn(f"Could not add to bucket. Invalid problem data: {prob}")
            return False
        
        index = self._calculateBucketIndex(prob.hour, prob.interval)
        if index == -1:
            Clogger.warn(f"Could not add to bucket. Invalid hour or interval: hour={prob.hour}, interval={prob.interval}")
            return False
        
        for dow in prob.dows:
            key = prob.getKey() # the key is the serverID::problemID, used later to trace back
            self.buckets[dow][index].add(key)
            
        Clogger.info(f"Successfully added problem {prob.problemID} to bucket.")
        return True
    
    # ADDING AND REMOVING SHOULD BE CALLED BY A SYNCRONIZER
    # TO ENSURE THAT THE BUCKET AND MODEL CONTAIN THE SAME DATA
    def removeFromBucket(self, prob: Problem) -> bool:
        if not prob.dows:
            Clogger.warn(f"Could not remove from bucket. Invalid problem data: {prob}")
            return False
        
        index = self._calculateBucketIndex(prob.hour, prob.interval)
        if index == -1:
            Clogger.warn(f"Could not remove from bucket. Invalid hour or interval: hour={prob.hour}, interval={prob.interval}")
            return False

        for dow in prob.dows:
            key = prob.getKey() # the key is the serverID::problemID, used later to trace back
            if key in self.buckets[dow][index]:
                self.buckets[dow][index].remove(key)
                Clogger.info(f"Successfully removed problem {prob.problemID} from bucket.")
            else:
                Clogger.warn(f"Could not remove problem {prob.problemID} from bucket. Not found.")
                return False
        return True


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