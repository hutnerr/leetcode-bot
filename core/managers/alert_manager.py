from utils import time_helper as timeh
from utils import problem_helper as probh

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
# TODO: Likely have to modify these return types when the discord integration is done
# ie make it easier to use with embeds
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
    # FIXME: If i also need a server id to alongside the channel ID to send, then i can just modify that here
    def collectProblemAlerts(self, dow: int, hour: int, interval: int) -> dict[int, str]:
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
                limit = 25 # limit the number of attempts to find a non-duplicate problem
                while server.isProblemDuplicate(slug) and limit > 0:
                    print(f"Duplicate problem {slug} found for server {sid}. Getting a new one.")
                    slug = self.problemManager.selectProblem(problem)
                    limit -= 1
            else:
                print(f"Allowing duplicates for server {sid}. Using problem {slug}.")
            
            if server.settings.postingChannelID is not None:
                channelIDsToSlug[server.settings.postingChannelID] = slug
            
            server.addPreviousProblem(slug)
            
        return channelIDsToSlug


    # collects the channel IDs and builds the alert message for the contest alerts
    # returns a tuple with the channel IDs and the alert message to send them
    def collectContestAlerts(self, timeAway: str, weekly: bool = False) -> tuple[list[int], str] | None:
        if weekly:
            contestType = "Weekly"
        else:
            contestType = "Biweekly"

        alertString = f"Upcoming {contestType} Contest in {timeh.minutesToHours(timeAway)}"

        serversToNotify = self.contestAlertBucket.getBucket(timeAway)
        channelIDs = [self.servers[server].settings.postingChannelID for server in serversToNotify if self.servers[server].settings.postingChannelID is not None]
        if not channelIDs:
            print("No channels to notify for contest alert.")
            return
        return (channelIDs, alertString)
        
    # these alerts all happen at a static time, so we can just get the channel IDs, build the alert message, and return them
    def collectStaticAlerts(self, alert: str):
        serversToNotify = self.staticBucket.getBucket(alert)
        if not serversToNotify:
            print(f"No servers to notify for static alert: {alert}.")
            return

        alertString = self.buildStaticAlertString(alert)
        if alertString is None:
            print(f"Failed to build alert string for static alert: {alert}.")
            return

        channelIDs = [self.servers[server].settings.postingChannelID for server in serversToNotify if self.servers[server].settings.postingChannelID is not None]
        if not channelIDs:
            print(f"No channels to notify for static alert: {alert}.")
            return
        return (channelIDs, alertString)
    
    def buildStaticAlertString(self, alert: str) -> str | None:
        # we have a contest
        if alert == "weekly" or alert == "biweekly":
            contestType = alert.capitalize()
            info = self.queryManager.getUpcomingContests()
            
            contests = info["data"]["upcomingContests"]
            title = None
            for contest in contests:
                if contest["title"].startswith(contestType):
                    title = contest["title"]
                    break
            
            # FIXME: Might have to -1 this. it deteremines how fast this updates
            if not title:
                print("Contest Query Failed")
                return None

            return f"{title} Opened!"

        # FIXME: also might need a delay on this 
        elif alert == "daily":
            slug = self.queryManager.getDailyProblem()["data"]["challenge"]["question"]["titleSlug"]
            return f"Daily Problem Released: {probh.slugToURL(slug)}"
        else:
            print(f"Invalid static alert type: {alert}.")
            return None