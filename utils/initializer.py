import os

from testing import generator as gen

from utils import json_helper as jsonh
from utils import file_helper as fileh

from buckets.contest_time_bucket import ContestTimeBucket
from buckets.problem_bucket import ProblemBucket
from buckets.static_time_bucket import StaticTimeBucket, StaticTimeAlert

from services.cache_service import CacheService
from services.problem_service import ProblemService
from services.query_service import QueryService

from mediators.synchronizer import Synchronizer
from mediators.alert_builder import AlertBuilder

from models.app import App
from models.server import Server
from models.user import User


# sets up and initializes the app 
class Initializer:
    @staticmethod
    def initApp(generate: bool = False, passedInServers: dict[int, Server] = None, nservers: int = 10, nproblems: int = 50, nusers=50) -> App:
        # if generate, gen servers
        # otherwise read from files
        if not passedInServers:
            if generate:
                servers = gen.generate(nservers, nproblems)
                users = gen.generateTestUsers(nusers)
            else:
                servers = readServersFromFiles()
                users = readUsersFromFiles()
                
        else:
            servers = passedInServers
            users = gen.generateTestUsers(nusers)

        buckets = setupBuckets(servers)
        problemBucket, staticTimeBucket, contestTimeBucket = buckets

        services = setupServices()
        cacheService, queryService, problemService = services
        
        mediators = setupMediators(servers, problemBucket, staticTimeBucket, contestTimeBucket, problemService, queryService)
        alertBuilder, synchronizer = mediators

        return App(servers, users, buckets, services, mediators)
        
    
def readServersFromFiles():
    # problems are saved within the servers json file so they're read in
    # when the server is built from JSON
    spath = os.path.join("data", "servers")
    servers: dict[int, Server] = dict()
    serverFiles = fileh.getFilesInDirectory(spath)
    for f in serverFiles:
        data = jsonh.readJSON(os.path.join(spath, f))
        serv = Server.buildFromJSON(data)
        servers[serv.serverID] = serv
    return servers
    
def readUsersFromFiles():
    upath = os.path.join("data", "users")
    users: dict[int, User] = dict()
    userFiles = fileh.getFilesInDirectory(upath)
    for f in userFiles:
        data = jsonh.readJSON(os.path.join(upath, f))
        user = User.buildFromJSON(data)
        users[user.discordID] = user
    return users
    
# ========================================================
# ================== Setup Buckets =======================
# ========================================================

def setupBuckets(servers):
    problemBucket = ProblemBucket()
    staticTimeBucket = StaticTimeBucket()
    contestTimeBucket = ContestTimeBucket()

    # the dowBucket has a ProblemBucket object for each day of the week
    def addServerToProblemBucket(server: Server):
        for problem in server.problems:
            if problem is not None:
                if not problemBucket.addToBucket(problem):
                    print("Failed to add problem to bucket:", problem)

    def addServerToStaticTimeBucket(server: Server):
        settings = server.settings
        if settings.weeklyContestAlerts:
            if not staticTimeBucket.addToBucket(StaticTimeAlert.WEEKLY_CONTEST, server.serverID):
                print("ADDING WEEKLY FAILED")
            
        if settings.biweeklyContestAlerts:
            if not staticTimeBucket.addToBucket(StaticTimeAlert.BIWEEKLY_CONTEST, server.serverID):
                print("ADDING BIWEEKLY FAILED")
            
        if settings.officialDailyAlerts:
            if not staticTimeBucket.addToBucket(StaticTimeAlert.DAILY_PROBLEM, server.serverID):
                print("ADDING DAILY FAILED")

    def addServerToContestTimeBucket(server: Server):
        settings = server.settings
        if settings.contestTimeAlerts and settings.contestTimeIntervals:
            for interval in settings.contestTimeIntervals:
                contestTimeBucket.addToBucket(interval, server.serverID)

    for server in servers.values():
        addServerToProblemBucket(server)
        addServerToStaticTimeBucket(server)
        addServerToContestTimeBucket(server)

    return (problemBucket, staticTimeBucket, contestTimeBucket)

# ========================================================
# ================== Setup Services ======================
# ========================================================

def setupServices():
    cacheService = CacheService()
    queryService = QueryService()
    problemService = ProblemService()
    return (cacheService, queryService, problemService)

# ========================================================
# ================== Setup Mediators =====================
# ========================================================

def setupMediators(servers, problemBucket, staticTimeBucket, contestTimeBucket, problemService, queryService):
    alertBuilder = AlertBuilder(servers, problemBucket, staticTimeBucket, contestTimeBucket, problemService, queryService)
    synchronizer = Synchronizer(servers, problemBucket, staticTimeBucket, contestTimeBucket)
    return (alertBuilder, synchronizer)

