import copy
from pyutils import Clogger

from models.problem import Problem
from models.server import Server

from buckets.problem_bucket import ProblemBucket
from buckets.contest_time_bucket import ContestTimeBucket
from buckets.static_time_bucket import StaticTimeBucket, StaticTimeAlert

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
        Clogger.info("Synchronizer initialized")

    # ==============================================
    # PROBLEMS
    # ==============================================

    # this ensures that the models store the same data as the buckets
    # adds a problem to where it belongs. ie the server and proper bucket
    def addProblem(self, problem: Problem) -> bool:
        pid = problem.problemID
        sid = problem.serverID
        
        if sid not in self.servers:
            Clogger.warn("Server ID not found in servers.")
            return False
        
        server = self.servers[sid]
        
        backupProblems = copy.deepcopy(server.problems)
        backupBucket = copy.deepcopy(self.problemBucket.buckets)
        
        # we have a problem with this id already, thus we need to remove it
        if problem in server.problems:
            problemToRemove = server.problems[pid]
            if not self.problemBucket.removeFromBucket(problemToRemove):
                Clogger.warn("Failed to remove problem from bucket.")
                return False # failed to remove
        
        # we either didn't have a problem to remove, or did and we removed it
        # we can safely add to the server and the buckets now
        if not server.addProblem(problem):
            Clogger.warn("Failed to add problem to server.")
            # if we fail to add to the server, we should revert the bucket
            # since we just removed a problem from it
            self.problemBucket.buckets = backupBucket
            return False # failed to add to server

        if not self.problemBucket.addToBucket(problem):
            # since we failed to add a problem to the bucket, we must revert the server
            server.problems = backupProblems
            Clogger.warn("Failed to add problem to bucket.")
            return False # failed to add to bucket
        
        return True

    # removes a problem from the server and the bucket
    def removeProblem(self, problem: Problem) -> bool:
        sid = problem.serverID
        
        if sid not in self.servers:
            Clogger.warn("Server ID not found in servers.")
            return False
        
        server = self.servers[sid]
        
        backupProblems = copy.deepcopy(server.problems)
        backupBucket = copy.deepcopy(self.problemBucket.buckets)
        
        # we have a problem with this id already, thus we need to remove it
        if problem not in server.problems:
            Clogger.warn("Problem not found in server.")
            return False # nothing to remove

        if not server.removeProblem(problem):
            # we failed to remove the problem, but we dont have to revert
            Clogger.warn("Failed to remove problem from server.")
            return False
        
        if not self.problemBucket.removeFromBucket(problem):
            server.problems = backupProblems
            self.problemBucket.buckets = backupBucket
            Clogger.warn("Failed to remove problem from bucket.")
            return False
        
        Clogger.info("Successfully removed problem {} from server {} and bucket.".format(problem.problemID, problem.serverID))
        return True
    
    # ==============================================
    # ALERT TIMES
    # ==============================================
    
    def changeAlertIntervals(self, serverID: int, newIntervals: list[int]) -> bool:
        if serverID not in self.servers:
            return False
                
        server = self.servers[serverID]
        
        # incase we encounter an error, we can revert
        backupIntervals = copy.deepcopy(server.settings.contestTimeIntervals)
        backupBucket = copy.deepcopy(self.contestTimeBucket.buckets)
        
        # get and remove the current intervals
        currentIntervals = server.settings.contestTimeIntervals
        if currentIntervals and len(currentIntervals) != 0:
            for interval in currentIntervals:
                if not self.contestTimeBucket.removeFromBucket(interval, serverID):
                    server.settings.contestTimeIntervals = backupIntervals
                    self.contestTimeBucket.buckets = backupBucket
                    Clogger.warn("Failed to remove contest time interval from bucket.")
                    return False
        
        # add the new intervals
        for interval in newIntervals:
            if not self.contestTimeBucket.addToBucket(interval, serverID):
                server.settings.contestTimeIntervals = backupIntervals
                self.contestTimeBucket.buckets = backupBucket
                Clogger.warn("Failed to add contest time interval to bucket.")
                return False
        
        server.settings.contestTimeIntervals = newIntervals
        server.toJSON() # save after we update the setting
        
        Clogger.info("Successfully updated contest time intervals for server {} to {}.".format(serverID, newIntervals))
        return True
    
    def changeContestAlertParticpation(self, serverID: int, participate: bool) -> bool:
        if serverID not in self.servers:
            Clogger.warn("Server ID not found in servers.")
            return False

        server = self.servers[serverID]
        serverSettings = server.settings
        
        backupSettings = copy.deepcopy(serverSettings)
        backupBucket = copy.deepcopy(self.contestTimeBucket.buckets)

        if serverSettings.contestTimeAlerts == participate:
            Clogger.info("Contest alert participation is already set to the desired value.")
            return True

        currentIntervals = server.settings.contestTimeIntervals
        if not currentIntervals:
            serverSettings.contestTimeAlerts = participate
            server.toJSON()
            Clogger.info("Server {} has no contest time intervals, so we just updated the setting without changing the buckets.".format(serverID))
            return True # no intervals to change, so we can just update the setting
            
        # if we now want to participate, add our intervals to the bucket
        # otherwise, remove them from the bucket 
        for interval in currentIntervals:
            if participate:
                if not self.contestTimeBucket.addToBucket(interval, serverID):
                    server.settings = backupSettings
                    self.contestTimeBucket.buckets = backupBucket
                    Clogger.warn("Failed to add contest time interval to bucket.")
                    return False
            else:
                if not self.contestTimeBucket.removeFromBucket(interval, serverID):
                    server.settings = backupSettings
                    self.contestTimeBucket.buckets = backupBucket
                    Clogger.warn(f"Failed to remove contest time interval {interval} from bucket.")
                    return False
              
        serverSettings.contestTimeAlerts = participate
        server.toJSON() # save after we update the setting
        Clogger.info("Successfully updated contest alert participation for server {} to {}.".format(serverID, participate))
        return True

    # ==============================================
    # STATIC ALERTS
    # ==============================================
    
    def changeStaticAlert(self, serverID: int, alert: StaticTimeAlert, participate: bool) -> bool:
        if serverID not in self.servers:
            Clogger.warn("Server ID not found in servers.")
            return False
        
        # update the server settings
        server = self.servers[serverID]
        serverSettings = server.settings
        
        backupSettings = copy.deepcopy(serverSettings)
        backupBucket = copy.deepcopy(self.staticTimeBucket.buckets)
        
        # update the setting if and only if it is not already set to 
        # what it is trying to be changed to 
        match (alert):
            case (StaticTimeAlert.WEEKLY_CONTEST):
                if serverSettings.weeklyContestAlerts == participate:
                    return True
                serverSettings.weeklyContestAlerts = participate
            case (StaticTimeAlert.BIWEEKLY_CONTEST):
                if serverSettings.biweeklyContestAlerts == participate:
                    return True
                serverSettings.biweeklyContestAlerts = participate
            case (StaticTimeAlert.DAILY_PROBLEM):
                if serverSettings.officialDailyAlerts == participate:
                    return True
                serverSettings.officialDailyAlerts = participate
            case _:
                Clogger.warn("Invalid alert")
                return False
        
        # if we got here, then we must update a bucket to reflect the change        
        # change the bucket to reflect
        # on participate, we want to add
        # if we do NOT want to participate, then we must remove
        if participate:
            if not self.staticTimeBucket.addToBucket(alert, serverID):
                server.settings = backupSettings
                self.staticTimeBucket.buckets = backupBucket
                Clogger.warn("Failed to add static time alert to bucket.")
                return False
        else:
            if not self.staticTimeBucket.removeFromBucket(alert, serverID):
                server.settings = backupSettings
                self.staticTimeBucket.buckets = backupBucket
                Clogger.warn("Failed to remove static time alert from bucket.")
                return False
        
        # self.staticTimeBucket.printBucketClean()
        server.toJSON() # save after we update the setting
        Clogger.info("Successfully updated static alert participation for server {} to {}.".format(serverID, participate))
        return True
