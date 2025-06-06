import os

from testing import generator as gen

from core.utils import json_helper as jsonh
from core.utils import file_helper as fileh

from core.buckets.contest_time_bucket import ContestTimeBucket
from core.buckets.problem_bucket import ProblemBucket
from core.buckets.static_time_bucket import StaticTimeBucket, StaticTimeAlert

from core.services.cache_service import CacheService
from core.services.problem_service import ProblemService
from core.services.query_service import QueryService

from core.mediators.synchronizer import Synchronizer
from core.mediators.alert_builder import AlertBuilder

from core.models.app import App
from core.models.server import Server


# sets up and initializes the app 
class Initializer:
    
    @staticmethod
    def initApp(generate: bool = False) -> App:
        # if generate, gen servers
        # otherwise read from files
        if generate:
            servers = gen.generate()
        else:
            servers = readFromFiles()
        
        buckets = setupBuckets(servers)
        problemBucket, staticTimeBucket, contestTimeBucket = buckets

        services = setupServices()
        cacheService, queryService, problemService = services
        
        mediators = setupMediators(servers, problemBucket, staticTimeBucket, contestTimeBucket, problemService)
        alertBuilder, synchronizer = mediators
        
        return App(servers, buckets, services, mediators)
        
    
def readFromFiles():
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
            staticTimeBucket.addToBucket(StaticTimeAlert.WEEKLY_CONTEST, server.serverID)
            
        if settings.biweeklyContestAlerts:
            staticTimeBucket.addToBucket(StaticTimeAlert.BIWEEKLY_CONTEST, server.serverID)
            
        if settings.officialDailyAlerts:
            staticTimeBucket.addToBucket(StaticTimeAlert.DAILY_PROBLEM, server.serverID)

    def addServerToContestTimeBucket(server: Server):
        settings = server.settings
        for interval in settings.contestAlertIntervals:
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

def setupMediators(servers, problemBucket, staticTimeBucket, contestTimeBucket, problemService):
    alertBuilder = AlertBuilder(servers, problemBucket, staticTimeBucket, contestTimeBucket, problemService)
    synchronizer = Synchronizer(servers, problemBucket, staticTimeBucket, contestTimeBucket)
    return (alertBuilder, synchronizer)

