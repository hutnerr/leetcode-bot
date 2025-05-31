from core.server import Server
from core.problem import Problem

from core.buckets.dow_buckets import DowBucket
from core.buckets.static_buckets import StaticBucket
from core.buckets.contest_alert_buckets import ContestAlertBucket

from core.managers.cache_manager import CacheManager
from core.managers.query_manager import QueryManager
from core.managers.problem_manager import ProblemManager

# this is the main manager that mostly everything is going to be handled through
# brings together the servers, buckets, and managers to handle alerts
class AlertManager:

    def __init__(self, servers: dict[int, Server], dowBucket: DowBucket, staticBucket: StaticBucket, contestAlertBucket: ContestAlertBucket, cacheManager: CacheManager, queryManager: QueryManager, problemManager: ProblemManager):
        self.servers = servers
        self.dowBucket = dowBucket
        self.staticBucket = staticBucket
        self.contestAlertBucket = contestAlertBucket
        self.cacheManager = cacheManager
        self.queryManager = queryManager
        self.problemManager = problemManager

    # collects all the channel ids and the slug of the problem that has beens selected based 
    # on the server settings and the problem bucket for the day of week, hour, and interval
    # returns it as a dict with the key is the channel ID and the value is the slug of the problem
    def handleProblemAlerts(self, dow: int, hour: int, interval: int) -> dict[int, str]:
        channelIDsToSlug = {}
        
        # get the bucket for the dow, hour, and interval.
        # these are the problems we want to notify the servers about
        bucket = self.dowBucket.getBucket(dow).getProblems(hour, interval)
        if bucket is None:
            print(f"No problems found for dow {dow}, hour {hour}, interval {interval}.")
            return
        
        for problem in bucket:
            sid, pid = map(int, problem.split("::"))
            
            if sid not in self.servers:
                print(f"Server {sid} not found for problem {pid}. Skipping.")
                continue
            
            # determine our server and problem 
            server = self.servers[sid]
            problem = server.problems[pid]
            if problem is None:
                print(f"Problem {pid} not found in server {sid}. Skipping.")
                continue
            
            slug = self.problemManager.selectProblem(problem)
            
            # if a problem is a duplicate, get a new one
            allowDuplicates = server.settings.duplicatesAllowed
            if not allowDuplicates:
                print("Checking for duplicates...")
                while server.isProblemDuplicate(slug):
                    print(f"Duplicate problem {slug} found for server {sid}. Getting a new one.")
                    slug = self.problemManager.selectProblem(problem)
            else:
                print(f"Allowing duplicates for server {sid}. Using problem {slug}.")
            
            if server.settings.postingChannelID is not None:
                channelIDsToSlug[server.settings.postingChannelID] = slug
            
        return channelIDsToSlug



    def handleContestAlert(self, timeAway: str):
        pass
