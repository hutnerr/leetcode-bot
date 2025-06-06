from buckets.contest_time_bucket import ContestTimeBucket
from buckets.problem_bucket import ProblemBucket
from buckets.static_time_bucket import StaticTimeBucket

from services.cache_service import CacheService
from services.problem_service import ProblemService
from services.query_service import QueryService

from mediators.synchronizer import Synchronizer
from mediators.alert_builder import AlertBuilder

from models.server import Server

# stores all of the key components
class App:
    def __init__(self, servers, buckets, services, mediators):
        self.servers: dict[int, Server] = servers
        
        self.problemBucket: ProblemBucket = buckets[0]
        self.staticTimeBucket: StaticTimeBucket = buckets[1]
        self.contestTimeBucket: ContestTimeBucket = buckets[2]
        
        self.cacheService: CacheService = services[0]
        self.queryService: QueryService = services[1]
        self.problemService: ProblemService = services[2]
        
        self.alertBuilder: AlertBuilder = mediators[0]
        self.synchronizer: Synchronizer = mediators[1]