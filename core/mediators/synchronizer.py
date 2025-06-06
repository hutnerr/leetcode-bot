from core.models.problem import Problem
from core.models.server import Server

from core.buckets.problem_bucket import ProblemBucket
from core.buckets.contest_time_bucket import ContestTimeBucket
from core.buckets.static_time_bucket import StaticTimeBucket, StaticTimeAlert

class Synchronizer:
    def __init__(self, 
                 servers: dict[int, Server], 
                 problemBucket: ProblemBucket, 
                 staticTimeBucket: StaticTimeBucket,
                 contestTimeBucket: ContestTimeBucket, 
                 ):
        self.servers = servers
        self.problemBucket = problemBucket
        self.contestTimeBucket = contestTimeBucket
        self.staticTimeBucket = staticTimeBucket

    # ==============================================
    # PROBLEMS
    # ==============================================

    # this ensures that the models store the same data as the buckets
    # adds a problem to where it belongs. ie the server and proper bucket
    def addProblem(self, problem: Problem):
        pid = problem.problemID
        sid = problem.serverID

        server = self.servers[sid]
        
        # we have a problem with this id already, thus we need to remove it
        if server.problems[pid] is not None:
            problemToRemove = server.problems[pid]
            if not self.dowBucket.removeFromBucket(problemToRemove):
                return False # failed to remove
        
        # we either didn't have a problem to remove, or did and we removed it
        # we can safely add to the server and the buckets now
        if not server.addProblem(problem):
            return False # failed to add to server
        
        if not self.dowBucket.addToBucket(problem):
            server.removeProblem(problem) # since we can't add to server
            return False # failed to add to bucket
        
        return True

    # removes a problem from the server and the bucket
    def removeProblem(self, problem: Problem):
        pid = problem.problemID
        sid = problem.serverID
        server = self.servers[sid]
        
        # we have a problem with this id already, thus we need to remove it
        if server.problems[pid] is None:
            return False # nothing to remove

        if not server.removeProblem(problem):
            return False
        
        if not self.dowBucket.removeFromBucket(problem):
            server.addProblem(problem) # add it back to the server, to keep it aligned
            return False
        
        return True
    
    # ==============================================
    # ALERT TIMES
    # ==============================================
    
    def changeAlertIntervals(self, serverID: int, newIntervals: list[int]) -> bool:
        if serverID not in self.servers:
            return False
        
        server = self.servers[serverID]
        
        # get and remove the current intervals
        currentIntervals = server.settings.contestAlertIntervals
        for interval in currentIntervals:
            if not self.contestTimeBucket.removeFromBucket(interval, server):
                return False
        
        # add the new intervals
        for interval in newIntervals:
            if not self.contestTimeBucket.addToBucket(interval, server):
                return False
        
        return True
    
    # ==============================================
    # STATIC ALERTS
    # ==============================================
    
    def changeStaticAlert(self, serverID: int, alert: StaticTimeAlert, participate: bool) -> bool:
        if serverID not in self.servers:
            return False
        
        # update the server settings
        server = self.servers[serverID]
        serverSettings = server.settings
        
        match (alert):
            case (StaticTimeAlert.WEEKLY_CONTEST):
                serverSettings.weeklyContestAlerts = participate
            case (StaticTimeAlert.BIWEEKLY_CONTEST):
                serverSettings.biweeklyContestAlerts = participate
            case (StaticTimeAlert.DAILY_PROBLEM):
                serverSettings.officialDailyAlerts = participate
            case _:
                return False
            
        server.toJSON() # save after we update the setting
        
        # change the bucket to reflect
        # on participate, we want to add
        # if we do NOT want to participate, then we must remove
        if participate:
            return self.staticTimeBucket.addToBucket(alert, serverID)
        else:
            return self.staticTimeBucket.removeFromBucket(alert, serverID)
            
        