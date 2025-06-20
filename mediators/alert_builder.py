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
    def buildContestAlerts(self, interval: int, alertType: AlertType) -> list[Alert]:
        alerts = []

        if alertType == AlertType.WEEKLY_CONTEST:
            contestType = "Weekly"
        elif alertType == AlertType.BIWEEKLY_CONTEST:
            contestType = "Biweekly"
        else:
            return []

        alertString = f"Upcoming {contestType} Contest in {timeh.minutesToHours(interval)}"

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
                "alertString" : alertString
            }
            alerts.append(Alert(alertType, server.serverID, server.settings.postingChannelID, info))
        
        return alerts
        
        
    # these alerts all happen at a static time, so we can just get the channel IDs, build the alert message, and return them
    def buildStaticAlerts(self, alert: StaticTimeAlert) -> list[Alert]:

        def buildStaticAlertString() -> str | None:
            # we have a contest
            if (alert == StaticTimeAlert.WEEKLY_CONTEST) or (alert == StaticTimeAlert.BIWEEKLY_CONTEST):
                contestType = alert.value.capitalize() # FIXME: uses the enum value, might be ugly
    
                info = self.queryService.getUpcomingContests()
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
            elif alert == StaticTimeAlert.DAILY_PROBLEM:
                slug = self.queryService.getDailyProblem()["data"]["challenge"]["question"]["titleSlug"]
                return f"Daily Problem Released: {probh.slugToURL(slug)}"
            else:
                return None # invalid alert
        
        alerts = []
        
        serversToNotify = self.staticTimeBucket.getBucket(alert)
        if not serversToNotify:
            return []

        alertString = buildStaticAlertString()
        if alertString is None:
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
            info = {
                "alertString" : alertString
            }
            alerts.append(Alert(alertType, server.serverID, server.settings.postingChannelID, info))

        return alerts
