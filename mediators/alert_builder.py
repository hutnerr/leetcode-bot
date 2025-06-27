from utils import datetime_helper as timeh
from utils import problem_helper as probh

from models.server import Server
from models.problem import Problem
from models.alert import Alert, AlertType

from services.problem_service import ProblemService
from services.query_service import QueryService

from buckets.problem_bucket import ProblemBucket
from buckets.static_time_bucket import StaticTimeBucket, StaticTimeAlert
from buckets.contest_time_bucket import ContestTimeBucket

# builds Alerts which contain the ServerID, ChannelID, and some info that will be expected 
# the info will be a dict, the keys/values will be context independent
class AlertBuilder:
    def __init__(self, 
                 servers: dict[int, Server], 
                 problemBucket: ProblemBucket, 
                 staticTimeBucket: StaticTimeBucket, 
                 contestTimeBucket: ContestTimeBucket, 
                 problemService: ProblemService,
                 queryService: QueryService
                 ):
        self.servers = servers
        self.problemBucket = problemBucket
        self.staticTimeBucket = staticTimeBucket
        self.contestTimeBucket = contestTimeBucket
        self.problemService = problemService
        self.queryService = queryService

    # collects all the server & channel ids and the slug of the problem that has beens selected based 
    # on the server settings and the problem bucket for the day of week, hour, and interval
    def buildProblemAlerts(self, dow: int, hour: int, interval: int) -> list[Alert]:
        alerts = []
        
        # the bucket problems are the problems we want to notify the servers about
        bucket = self.problemBucket.getBucket(dow, hour, interval)
        if bucket is None:
            return []
        
        # sid = serverID, pid = problemID
        for problem in bucket:
            sid, pid = map(int, problem.split("::")) # cast to ints
            
            if sid not in self.servers: # couldn't find the serverID
                continue
            
            # determine our server and problem 
            server = self.servers[sid]
            problem = server.problems[pid]
            if problem is None: # couldn't find the problemID
                continue
            
            slug, difficulty = self.problemService.selectProblem(problem)
            
            # if a problem is a duplicate, get a new one
            allowDuplicates = server.settings.duplicatesAllowed
            if not allowDuplicates:
                limit = 25 # limit the number of attempts to find a non-duplicate problem
                while server.isProblemDuplicate(slug) and limit > 0:
                    slug = self.problemManager.selectProblem(problem)
                    limit -= 1

            if server.settings.postingChannelID is not None:
                info = {
                    "slug" : slug,
                    "pid" : pid,
                    "difficulty" : difficulty
                }
                alerts.append(Alert(AlertType.PROBLEM, server.serverID, server.settings.postingChannelID, info))
            
        return alerts


    # collects the server & channel IDs and builds the alert message for the contest alerts
    def buildContestAlerts(self, interval: int, alertType: AlertType, contestAlertType: AlertType) -> list[Alert]:
        alerts = []

        if contestAlertType == AlertType.WEEKLY_CONTEST:
            contestType = "Weekly"
        elif contestAlertType == AlertType.BIWEEKLY_CONTEST:
            contestType = "Biweekly"
        else:
            return []

        info = self.queryService.getUpcomingContests()
        contests = info["data"]["upcomingContests"]
        title = None
        titleSlug = None
        for contest in contests:
            if contest["title"].startswith(contestType):
                title = contest["title"]
                titleSlug = contest["titleSlug"]
                break
        
        url = f"https://leetcode.com/contest/{titleSlug}/"
        
        if not title or not titleSlug:
            # if we don't have a contest, we can't build an alert
            print("Contest Query Failed")
            return []
        
        # FIXME: Might have to -1 this. it deteremines how fast this updates
        if not title or not titleSlug:
            print("Contest Query Failed")
            return None

        alertString = f"[{title}]({url}) is upcoming in **{timeh.minutesToHours(interval)}**! Remember to register and prepare!"

        serversToNotify = self.contestTimeBucket.getBucket(interval)
        if not serversToNotify: # no servers to notify
            return []
        
        for serverID in serversToNotify:
            server = self.servers[serverID]            
            
            # we may be in the bucket, but have the setting turned off
            # in this case, just ignore
            if not server.settings.contestTimeAlerts:
                continue
            
            info = {
                "alertString" : alertString,
                "url" : f"https://leetcode.com/contest/{titleSlug}/",
            }
            alerts.append(Alert(alertType, server.serverID, server.settings.postingChannelID, info))
        
        return alerts
        
        
    # these alerts all happen at a static time, so we can just get the channel IDs, build the alert message, and return them
    def buildStaticAlerts(self, alert: StaticTimeAlert) -> list[Alert]:

        def buildStaticAlertInfo() -> dict | None:
            # we have a contest
            if (alert == StaticTimeAlert.WEEKLY_CONTEST) or (alert == StaticTimeAlert.BIWEEKLY_CONTEST):
                contestType = alert.value.capitalize() # FIXME: uses the enum value, might be ugly
    
                info = self.queryService.getUpcomingContests()
                contests = info["data"]["upcomingContests"]
                title = None
                titleSlug = None
                for contest in contests:
                    if contest["title"].startswith(contestType):
                        title = contest["title"]
                        titleSlug = contest["titleSlug"]
                        break

                # FIXME: Might have to -1 this. it deteremines how fast this updates
                if not title or not titleSlug:
                    print("Contest Query Failed")
                    return None

                url = f"https://leetcode.com/contest/{titleSlug}/"
                alertString = f"LeetCode [{title}]({url}) is now open!"

            # FIXME: also might need a delay on this 
            elif alert == StaticTimeAlert.DAILY_PROBLEM:
                titleSlug = self.queryService.getDailyProblem()["data"]["challenge"]["question"]["titleSlug"]
                url = probh.slugToURL(titleSlug)
                alertString = f"Today's daily problem is now available! It is [{probh.slugToTitle(titleSlug)}]({url})."
            else:
                return None # invalid alert
            
            info = {
                "alertString" : alertString,
                "url" : url
            }
            return info
        
        alerts = []
        
        serversToNotify = self.staticTimeBucket.getBucket(alert)
        if not serversToNotify:
            return []

        alertInfo = buildStaticAlertInfo()
        if alertInfo is None:
            return []

        match (alert):
            case StaticTimeAlert.WEEKLY_CONTEST:
                alertType = AlertType.WEEKLY_CONTEST
            case StaticTimeAlert.BIWEEKLY_CONTEST:
                alertType = AlertType.BIWEEKLY_CONTEST
            case StaticTimeAlert.DAILY_PROBLEM:
                alertType = AlertType.DAILY_PROBLEM
            case _:
                return []

        for serverID in serversToNotify:
            server = self.servers[serverID]
            info = alertInfo
            alerts.append(Alert(alertType, server.serverID, server.settings.postingChannelID, info))

        return alerts
