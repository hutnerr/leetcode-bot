from core.buckets.dow_buckets import DowBucket
from core.server import Server
from core.problem import Problem

class ProblemManager:
    
    def __init__(self, servers: dict[int, Server], dowBucket: DowBucket):
        self.servers = servers
        self.dowBucket = dowBucket

    # adds a problem to where it belongs. ie the server and proper bucket
    def addProblem(self, problem: Problem):
        pid = problem.problemID
        sid = problem.serverID

        server = self.servers[sid]
        
        # we have a problem with this id already, thus we need to remove it
        if server.problems[pid] is not None:
            problemToRemove = server.problems[pid]
            if not self.dowBucket.removeFromBucket(problemToRemove):
                print("Failed to remove from bucket")
                return False
        
        # we either didn't have a problem to remove, or did and we removed it
        # we can safely add to the server and the buckets now
        if not server.addProblem(problem):
            print("Failed to add problem")
            return False
        
        if not self.dowBucket.addToBucket(problem):
            print("Failed to add to bucket")
            return False
        
        return True
    
