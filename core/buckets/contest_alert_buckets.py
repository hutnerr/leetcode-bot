# handles alerts for contests
# ie you can set intervals for how far away you want to be notified about contests
# ie 15 minutes, 30 minutes, 1hr, 2hr, 6hr, 12hr, 24hr

from core.server import Server

class ContestAlertBucket:
    def __init__(self):
        self.buckets: dict[int, list[int]] = {
            15: [],
            30: [],
            60: [],
            120: [],
            360: [],
            720: [],
            1440: []
        }

    def __str__(self) -> str:
        return str(self.buckets)

    def printBucketClean(self):
        print("Contest Alert Buckets:")
        for interval, servers in self.buckets.items():
            print(f"  {interval} minutes: {servers}")

    def addToBucket(self, interval: int, serverID: int):
        if interval in self.buckets:
            if serverID not in self.buckets[interval]:
                self.buckets[interval].append(serverID)

    def removeFromBucket(self, interval: int, serverID: int):
        if interval in self.buckets:
            if serverID in self.buckets[interval]:
                self.buckets[interval].remove(serverID)

    def getBucket(self, interval: int) -> list[int]:
        return self.buckets.get(interval, [])

    def notifyServers(self, servers: dict[int, Server], interval: int):
        if interval not in self.buckets:
            print(f"Invalid interval: {interval}")
            return

        serversToNotify = self.buckets[interval]
        if not serversToNotify:
            print(f"No servers in {interval} minute bucket.")
            return

        for serverID in serversToNotify:
            server = servers.get(serverID)
            if server:
                server.handleContestAlert(interval)
                # print("Notifying server", serverID, "for interval", interval)
                # server.handleProblemNotification(interval)
