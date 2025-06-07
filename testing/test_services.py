import os

from testing.generator import GeneratedServers

from utils.initializer import Initializer
from utils import problem_helper as probh

from models.app import App
from models.problem import Problem

from services.cache_service import CacheService
from services.problem_service import ProblemService
from services.query_service import QueryService

# services integration testing
def makeApp() -> App:
    servers = GeneratedServers().collectServers()
    return Initializer.initApp(passedInServers=servers)
    
def testCacheService() -> bool:
    app = makeApp()
    cacheService: CacheService = app.cacheService
    
    assert cacheService, "App's cacheService was None"

    # initCache testing is done in constructor
    # caching an actual problem done together alongside the query service

    # test existsInCache
    assert cacheService.existsInCache("two-sum"), "CacheService existsInCache returned False for a problem that should exist"
    assert not cacheService.existsInCache("TESTTEST"), "CacheService existsInCache returned True for a problem that should NOT exist"

    # test getFromCache
    assert cacheService.getFromCache("two-sum"), "Should exist, but got nothing from getFromCache"
    assert not cacheService.getFromCache("TESTTEST"), "Should NOT exist, but got a result that wasn't None"

    return True


def testProblemService() -> bool:
    app = makeApp()
    problemService: ProblemService = app.problemService

    assert problemService, "App's problemService was None"

    # the service Setup will be tested through being able to properly select a problem
    testServer = app.servers[2]
    p1 = testServer.problems[1] # easy, not premium
    p2 = testServer.problems[2] # medium, premium
    p3 = testServer.problems[3] # hard, either

    assert not (p1 is None or p2 is None or p3 is None), "One of the problems is None, but it shouldn't be"
    
    p1slug, p1dif = problemService.selectProblem(p1)
    p2slug, p2dif = problemService.selectProblem(p2)
    p3slug, p3dif = problemService.selectProblem(p3)

    assert p1slug and p2slug and p3slug, "Failed in problem selection"
    
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
    assert not problemService.selectProblem(invalidProblem), "Selected a problem with an invalid difs"

    # testing with and None difs
    invalidProblem = Problem(pid=1, sid=2, difs=None, dow=1, hour=1, interval=1, premium=0)
    assert not problemService.selectProblem(invalidProblem), "Selected a problem with an None difs list"

    return True


def testQueryService() -> bool:
    USERNAME = "hutnerr"
    BADUSERNAME = "RANDOMTRASHTESTING123"
    PROBLEM_SLUG = "two-sum"
    
    app = makeApp()
    queryService: QueryService = app.queryService

    assert queryService, "App's queryService was None"

    # daily problem query test
    dailyProblemInfo = queryService.getDailyProblem()
    assert "data" in dailyProblemInfo, "Daily Problem Info Query Failed"

    # get user recent accepted submissions test
    # test w a limit and with no limit
    recentUserAcceptedInfo = queryService.getUserRecentAcceptedSubmissions(USERNAME)
    assert len(recentUserAcceptedInfo["data"]["recentAcSubmissionList"]) == 10, "Recent Accepted Submissions not 10 on no limit defined"

    recentUserAcceptedInfo = queryService.getUserRecentAcceptedSubmissions(USERNAME, 1)
    assert len(recentUserAcceptedInfo["data"]["recentAcSubmissionList"]) == 1, "Recent Accepted Submissions not 1 on a limit of 1"

    recentUserAcceptedInfo = queryService.getUserRecentAcceptedSubmissions(BADUSERNAME)
    assert not recentUserAcceptedInfo["data"]["recentAcSubmissionList"], "Recent Accepted Submissions is not None on an invalid account"

    # recentUserAcceptedInfo = queryService.getUserRecentAcceptedSubmissions(USERNAME, -1) # this just returns max limit
    # recentUserAcceptedInfo = queryService.getUserRecentAcceptedSubmissions(USERNAME, 0) # this also returns max limit
    
    # get user profile test
    userProfileInfo = queryService.getUserProfile(USERNAME)
    assert "errors" not in userProfileInfo, "Query failed. No match"

    assert userProfileInfo["data"]["matchedUser"]["username"] == USERNAME, "Wrong Username"
    
    userProfileInfo = queryService.getUserProfile(BADUSERNAME)
    assert "errors" in userProfileInfo, "Found a user for the Bad User Name"

    # get question info
    questionInfo = queryService.getQuestionInfo(PROBLEM_SLUG)
    assert questionInfo["data"]["question"], "Good question slug got a bad result"

    questionInfo = queryService.getQuestionInfo("DONT EXIST")
    assert not questionInfo["data"]["question"], "Bad question slug got a valid result"

    # get upcoming contests
    upcomingContestInfo = queryService.getUpcomingContests()
    assert "errors" not in upcomingContestInfo, "Failed getting Upcoming Contest Info"

    return True


def testSubmitter() -> bool:
    # add a user, test if its actually in users
    # whatveer else needs done 
    pass


def lifecycleTest() -> bool:
    app = makeApp()
    queryService = app.queryService
    problemService = app.problemService
    cacheService = app.cacheService

    problem = Problem(pid=1, sid=2, difs="easy-medium", dow=1, hour=1, interval=1, premium=0) # easy/medium, free problem
    problemSlug, problemDifficulty = problemService.selectProblem(problem)
    
    if cacheService.existsInCache(problemSlug):
        problemInfo = cacheService.getFromCache(problemSlug)
    else:
        path = os.path.join("data", "problem_cache", f"{problemSlug}.json")
        assert not os.path.exists(path), "Path exists BEFORE caching it"
        problemInfo = queryService.getQuestionInfo(problemSlug)
        cacheService.cacheProblem(problemInfo)
        assert os.path.exists(path), "Problem file does not exist after caching"

    problemDif = problemInfo["data"]["question"]["difficulty"]
    assert problemDif in ["Medium", "Easy"], "Problem is something besides the set easy-medium"

    problemPremium = problemInfo["data"]["question"]["isPaidOnly"]
    assert not problemPremium, "Problem is premium. It should be free"

    problemSlug = "two-sum"
    if cacheService.existsInCache(problemSlug):
        problemInfo = cacheService.getFromCache(problemSlug)
    else:
        assert False, "Failed on the cache hit for two-sum"

    return True
