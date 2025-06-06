from core.buckets.contest_time_bucket import ContestTimeBucket
from core.buckets.problem_bucket import ProblemBucket
from core.buckets.static_time_bucket import StaticTimeBucket

from core.services.cache_service import CacheService
from core.services.problem_service import ProblemService
from core.services.query_service import QueryService

from core.mediators.synchronizer import Synchronizer
from core.mediators.alert_builder import AlertBuilder

from core.models.server import Server

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