from enum import Enum

# this bucket is for things that will always happen at a static defined time. 
# if a server is added to the bucket, then it wants to be notified about this event
class StaticTimeBucket:
    def __init__(self):
        self.buckets: dict[str, set[int]] = {
            StaticTimeAlert.WEEKLY_CONTEST: set(),
            StaticTimeAlert.BIWEEKLY_CONTEST: set(),
            StaticTimeAlert.DAILY_PROBLEM: set()
        }
    
    def __str__(self) -> str:
        return str(self.buckets)
    
    # ADDING AND REMOVING SHOULD BE CALLED BY A SYNCRONIZER
    # TO ENSURE THAT THE BUCKET AND MODEL CONTAIN THE SAME DATA
    def addToBucket(self, bucketType: "StaticTimeAlert", serverID: int) -> bool:
        if bucketType in self.buckets:
            if serverID not in self.buckets[bucketType]:
                self.buckets[bucketType].add(serverID)
                return True
        return False
    
    # ADDING AND REMOVING SHOULD BE CALLED BY A SYNCRONIZER
    # TO ENSURE THAT THE BUCKET AND MODEL CONTAIN THE SAME DATA
    def removeFromBucket(self, bucketType: "StaticTimeAlert", serverID: int) -> bool:
        if bucketType in self.buckets:
            if serverID in self.buckets[bucketType]:
                self.buckets[bucketType].remove(serverID)
                return True
        return False
    
    # returns a list of all of the servers in the bucketType
    def getBucket(self, bucketType: "StaticTimeAlert") -> list[int] | None:
        return self.buckets.get(bucketType, [None])


   # FIXME: For testing, delete when product complete
    def printBucketClean(self):
        print("Static Buckets:")
        print(f"Weekly Contest: {self.buckets[StaticTimeAlert.WEEKLY_CONTEST]}")
        print(f"Biweekly Contest: {self.buckets[StaticTimeAlert.BIWEEKLY_CONTEST]}")
        print(f"Daily Problem: {self.buckets[StaticTimeAlert.DAILY_PROBLEM]}")
        
# enum to use instead of strings
class StaticTimeAlert(Enum):
    WEEKLY_CONTEST = "weekly"
    BIWEEKLY_CONTEST = "biweekly"
    DAILY_PROBLEM = "daily"