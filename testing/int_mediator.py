import os

from testing.generator import GeneratedServers

from utils.initializer import Initializer
from utils import problem_helper as probh

from models.app import App
from models.problem import Problem

from services.cache_service import CacheService
from services.problem_service import ProblemService
from services.query_service import QueryService

from buckets.static_time_bucket import StaticTimeAlert

# mediator integration testing
def makeApp() -> App:
    servers = GeneratedServers().collectServers()
    return Initializer.initApp(passedInServers=servers)


def testAlertBuilder() -> bool:
    app = makeApp()
    
    alertBuilder = app.alertBuilder
    assert alertBuilder is not None, "App's alertBuilder was None"

    # THE STATIC GENERATED TESTING SERVER INFO:
    # server1:  
    # - weekly, biweekly, daily, contesttime, [15, 30] intervals      
    # - 3 problems: all dow=1, hour=1, interval=1
    
    # server2:
    # - no alerts
    # - 5 problems: p1 is dow=1, hour=1, p2 is dow=2, hour=2, etc. all interval is 0
    
    # server3:
    # - weekly, contesttime, [] empty intervals
    # - 5 problems: all dow=1, hour=1, interval=1
    
    # test for buckets that SHOULD have stuff in them, and then for buckets that
    # i know will NOT have anything in them
    
    # app.problemBucket.printBucketClean()
    
    # should work: valid times,
    # shouldn't work, invalid dow, invalid hour, invalid interval, individually
    # problemAlerts = alertBuilder.buildProblemAlerts()
    
    # test what happens for a server that wants alerts but has no intervals set
    # contestAlerts = alertBuilder.buildContestAlerts()
    
    # weekyStaticAlerts = alertBuilder.buildContestAlerts(StaticTimeAlert.WEEKLY_CONTEST)
    # biweekyStaticAlerts = alertBuilder.buildContestAlerts(StaticTimeAlert.BIWEEKLY_CONTEST)
    # dailyStaticAlerts = alertBuilder.buildContestAlerts(StaticTimeAlert.DAILY_PROBLEM)
    
    return True


def testSyncrhonzier() -> bool:
    # adding a problem to a server that has a full 5 problems
    return True