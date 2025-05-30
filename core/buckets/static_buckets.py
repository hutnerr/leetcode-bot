# uses a dictionary to store buckets
# the key is the type of bucket, the value is a list of servers that need to be notified
# this works since the times are static, and servers just need to opt in/out
# as of now, the buckets are:
# weekly, biweekly, daily
# representing if a server wants to be notified about weekly contests, biweekly contests, or daily problems
# on the static times that they are released
from core.server import Server

class StaticBucket:
    def __init__(self):
        self.buckets: dict[str, list[int]] = {
            "weekly": [],
            "biweekly": [],
            "daily": []
        }
    
    def __str__(self) -> str:
        return str(self.buckets)
    
    # for testing/debugging
    def printBucketClean(self):
        print("Static Buckets:")
        print(f"Weekly: {self.buckets['weekly']}")
        print(f"Biweekly: {self.buckets['biweekly']}")
        print(f"Daily: {self.buckets['daily']}")

    # =================ADD TO BUCKETS===============================
    def addToWeeklyBucket(self, serverID: int):
        if serverID not in self.buckets["weekly"]:
            self.buckets["weekly"].append(serverID)
            
    def addToBiweeklyBucket(self, serverID: int):
        if serverID not in self.buckets["biweekly"]:
            self.buckets["biweekly"].append(serverID)
    
    def addToDailyBucket(self, serverID: int):
        if serverID not in self.buckets["daily"]:
            self.buckets["daily"].append(serverID)
        
    # =================REMOVE FROM BUCKETS===============================
    def removeFromWeeklyBucket(self, serverID: int):
        if serverID in self.buckets["weekly"]:
            self.buckets["weekly"].remove(serverID)
            
    def removeFromBiweeklyBucket(self, serverID: int):
        if serverID in self.buckets["biweekly"]:
            self.buckets["biweekly"].remove(serverID)
    
    def removeFromDailyBucket(self, serverID: int):
        if serverID in self.buckets["daily"]:
            self.buckets["daily"].remove(serverID)
    
    # =================GETTERS========================================
    def getWeeklyBucket(self) -> list[int]:
        return self.buckets["weekly"]
    
    def getBiweeklyBucket(self) -> list[int]:
        return self.buckets["biweekly"]
    
    def getDailyBucket(self) -> list[int]:
        return self.buckets["daily"]
    

    # =================OBSERVER HANDLING================================

    # bucketType is one of "weekly", "biweekly", or "daily"
    def notifyServers(self, servers:dict[int, Server], bucketType: str):
        if bucketType not in self.buckets:
            print(f"Invalid bucket type: {bucketType}")
            return
        
        serversToNotify = self.buckets[bucketType]
        if not serversToNotify:
            print(f"No servers in {bucketType} bucket.")
            return

        for serverID in serversToNotify:
            server = servers.get(serverID)
            if server:
                server.handleStaticAlert(bucketType)
