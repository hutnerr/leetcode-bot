# handles alerts for contest time away
# ie you can set intervals for how far away you want to be notified about contests
# ie 15 minutes, 30 minutes, 1hr, 2hr, 6hr, 12hr, 24hr
# this does NOT handle the alerts for when the contest actually happens, just the times leading up to it
class ContestTimeBucket:
    def __init__(self):
        self.buckets: dict[int, set[int]] = {
            15: set(),     # 15 mins
            30: set(),     # 30 mins
            60: set(),     # 1 hr
            120: set(),    # 2 hrs
            360: set(),    # 6 hrs
            720: set(),    # 12 hrs
            1440: set()    # 1 day
        }

    def __str__(self) -> str:
        return str(self.buckets)

    # ADDING AND REMOVING SHOULD BE CALLED BY A SYNCRONIZER
    # TO ENSURE THAT THE BUCKET AND MODEL CONTAIN THE SAME DATA
    def addToBucket(self, interval: int, serverID: int) -> bool:
        if interval in self.buckets:
            if serverID not in self.buckets[interval]:
                self.buckets[interval].add(serverID)
                return True
        return False

    # ADDING AND REMOVING SHOULD BE CALLED BY A SYNCRONIZER
    # TO ENSURE THAT THE BUCKET AND MODEL CONTAIN THE SAME DATA
    def removeFromBucket(self, interval: int, serverID: int) -> bool:
        if interval in self.buckets:
            if serverID in self.buckets[interval]:
                self.buckets[interval].remove(serverID)
                return True
        return False

    def getBucket(self, interval: int) -> list[int] | None:
        return self.buckets.get(interval, None)
    
    
    # FIXME: For testing, delete when product complete
    def printBucketClean(self):
        print("Contest Alert Buckets:")
        for interval, servers in self.buckets.items():
            print(f"  {interval} minutes: {servers}")
