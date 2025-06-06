import os

from testing.generator import GeneratedServers

from core.utils.initializer import Initializer
from core.utils import problem_helper as probh

from core.models.app import App
from core.models.problem import Problem

from core.services.cache_service import CacheService
from core.services.problem_service import ProblemService
from core.services.query_service import QueryService

# services integration testing
def makeApp() -> App:
    servers = GeneratedServers().collectServers()
    return Initializer.initApp(passedInServers=servers)
    
def testCacheService() -> tuple[bool, str]:
    app = makeApp()
    cacheService: CacheService = app.cacheService    
    
    if not cacheService:
        return (False, "App's cacheService was None")

    # initCache testing is done in constructor
    # caching an actual problem done together alongside the query service
    
    # exists in cache. two-sum should exist
    exists = cacheService.existsInCache("two-sum") # should exist
    if not exists:
        return (False, "Problem that should exist in cache return as if it does not")
    
    exists = cacheService.existsInCache("TESTTEST") # shouldn't exist
    if exists:
        return (False, "Problem that should NOT exist, returned as if it did")
    
    # test getting from cache
    problemInfo = cacheService.getFromCache("two-sum") # should exist
    if not problemInfo:
        return (False, "Should exist, but got nothing from getFromCache")
    
    problemInfo = cacheService.getFromCache("TESTTEST") # shouldn't exist
    if problemInfo:
        return (False, "Should NOT exist, but got a result that wasn't None")

    return (True, "All Good!")


def testProblemService() -> tuple[bool, str]:
    app = makeApp()
    problemService: ProblemService = app.problemService

    if not problemService:
        return (False, "App's problemService was None")

    # the service Setup will be tested through being able to properly select a problem
    testServer = app.servers[2]
    p1 = testServer.problems[1] # easy, not premium
    p2 = testServer.problems[2] # medium, premium
    p3 = testServer.problems[3] # hard, either
        
    if (not p1) or (not p2) or (not p3):
        return (False, "Failed getting the problems from the test server")
    
    p1slug = problemService.selectProblem(p1)
    p2slug = problemService.selectProblem(p2)
    p3slug = problemService.selectProblem(p3)

    if (not p1slug) or (not p2slug) or (not p3slug):
        return (False, "Failed in problem selection")
    
    # manually check these for now
    # adaptive testing done in the all together testing
    p1link = probh.slugToURL(p1slug)
    p2link = probh.slugToURL(p2slug)
    p3link = probh.slugToURL(p3slug)
    
    # print(p1link)
    # print(p2link)
    # print(p3link)
    
    # testing with an empty difs
    invalidProblem = Problem(pid=1, sid=2, difs=[], dow=1, hour=1, interval=1, premium=0)
    invalidSlug = problemService.selectProblem(invalidProblem)
    if invalidSlug:
        return (False, "Selected a problm with an invalid difs")
    
    # testing with and None difs
    invalidProblem = Problem(pid=1, sid=2, difs=None, dow=1, hour=1, interval=1, premium=0)
    invalidSlug = problemService.selectProblem(invalidProblem)
    if invalidSlug:
        return (False, "Selected a problm with an None difs list")
    
    return (True, "All Good!")


def testQueryService() -> tuple[bool, str]:
    USERNAME = "hutnerr"
    BADUSERNAME = "RANDOMTRASHTESTING123"
    PROBLEM_SLUG = "two-sum"
    
    app = makeApp()
    queryService: QueryService = app.queryService

    if not queryService:
        return (False, "App's queryService was None")
    
    # daily problem query test
    dailyProblemInfo = queryService.getDailyProblem()
    if "data" not in dailyProblemInfo:
        return (False, "Daily Problem Info Query Failed")

    # get user recent accepted submissions test
    # test w a limit and with no limit
    recentUserAcceptedInfo = queryService.getUserRecentAcceptedSubmissions(USERNAME)
    if len(recentUserAcceptedInfo["data"]["recentAcSubmissionList"]) != 10:
        return (False, "Recent Accepted Submissions not 10 on no limit defined")
    
    recentUserAcceptedInfo = queryService.getUserRecentAcceptedSubmissions(USERNAME, 1)
    if len(recentUserAcceptedInfo["data"]["recentAcSubmissionList"]) != 1:
        return (False, "Recent Accepted Submissions not 1 on a limit of 1")
    
    recentUserAcceptedInfo = queryService.getUserRecentAcceptedSubmissions(BADUSERNAME)
    if recentUserAcceptedInfo["data"]["recentAcSubmissionList"]:
        return (False, "Recent Accepted Submissions is not None on an invalid account")
    
    # recentUserAcceptedInfo = queryService.getUserRecentAcceptedSubmissions(USERNAME, -1) # this just returns max limit
    # recentUserAcceptedInfo = queryService.getUserRecentAcceptedSubmissions(USERNAME, 0) # this also returns max limit
    
    # get user profile test
    userProfileInfo = queryService.getUserProfile(USERNAME)
    if "errors" in userProfileInfo:
        return (False, "Query failed. No match")
        
    if userProfileInfo["data"]["matchedUser"]["username"] != USERNAME:
        return (False, "Wrong Username")
    
    userProfileInfo = queryService.getUserProfile(BADUSERNAME)
    if "errors" not in userProfileInfo:
        return (False, "Found a user for the Bad User Name")
    
    # get question info
    questionInfo = queryService.getQuestionInfo(PROBLEM_SLUG)
    if not questionInfo["data"]["question"]:
        return (False, "Good question slug got a bad result")
    
    questionInfo = queryService.getQuestionInfo("DONT EXIST")
    if questionInfo["data"]["question"]:
        return (False, "Bad question slug got a valid result")
    
    # get upcoming contests
    upcomingContestInfo = queryService.getUpcomingContests()
    if "errors" in upcomingContestInfo:
        return (False, "Failed getting Upcoming Contest Info")
    
    return (True, "All Good!")

def lifecycleTest():
    app = makeApp()
    queryService = app.queryService
    problemService = app.problemService
    cacheService = app.cacheService

    problem = Problem(pid=1, sid=2, difs="easy-medium", dow=1, hour=1, interval=1, premium=0) # easy/medium, free problem
    problemSlug = problemService.selectProblem(problem)
    
    if cacheService.existsInCache(problemSlug):
        problemInfo = cacheService.getFromCache(problemSlug)
    else:
        path = os.path.join("data", "problem_cache", f"{problemSlug}.json")
        if os.path.exists(path):
            return (False, "Path exists BEFORE caching it")
        problemInfo = queryService.getQuestionInfo(problemSlug)
        cacheService.cacheProblem(problemInfo)
        if not os.path.exists(path):
            return (False, "Problem file does not exist after caching")

    problemDif = problemInfo["data"]["question"]["difficulty"]
    if (problemDif != "Medium") and (problemDif != "Easy"):
        return (False, "Problem is something besides the set easy-medium")
    
    problemPremium = problemInfo["data"]["question"]["isPaidOnly"]
    if problemPremium:
        return (False, "Problem is premium. It should be free")

    problemSlug = "two-sum"
    if cacheService.existsInCache(problemSlug):
        problemInfo = cacheService.getFromCache(problemSlug)
    else:
        return (False, "Failed on the cache hit for two-sum")
    
    return (True, "All Good!")
