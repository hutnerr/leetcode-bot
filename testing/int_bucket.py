from testing.generator import GeneratedServers
from utils.initializer import Initializer
from models.app import App
import copy

from buckets.static_time_bucket import StaticTimeAlert

# bucket integration testing
def makeApp() -> App:
    servers = GeneratedServers().collectServers()
    return Initializer.initApp(passedInServers=servers)

# static time bucket
def testStaticTimeBucket() -> bool:
    app = makeApp()
    
    staticTimeBucket = app.staticTimeBucket
    assert staticTimeBucket is not None, "App's staticTimeBucket is None"
    
    # staticTimeBucket.printBucketClean()
    initialBucket = copy.deepcopy(staticTimeBucket.buckets)
    
    # ===== TESTING GET BUCKET =====
    weeklyBucket = staticTimeBucket.getBucket(StaticTimeAlert.WEEKLY_CONTEST)
    assert weeklyBucket, "Weekly bucket is None"
    
    weeklyExpected = set([1, 3])
    assert weeklyBucket == weeklyExpected, "Weekly did not match the expected"

    biweeklyBucket = staticTimeBucket.getBucket(StaticTimeAlert.BIWEEKLY_CONTEST)
    assert biweeklyBucket, "Biweekly bucket is None"

    biweeklyExpected = set([1])
    assert biweeklyBucket == biweeklyExpected, "Biweekly did not match the expected"

    dailyBucket = staticTimeBucket.getBucket(StaticTimeAlert.DAILY_PROBLEM)
    assert dailyBucket, "Daily bucket is None"

    dailyExpected = set([1])
    assert dailyBucket == dailyExpected, "Daily did not match the expected"

    # FOR ADD TO AND REMOVE FROM, USING ALONE WILL MAKE INCONSISTENCIES WITH SERVER INTERALLY
    # USE THE SYNCHRONIZER TO PREVENT IN REAL USE

    # ===== TESTING ADD TO BUCKET =====
    assert not staticTimeBucket.addToBucket(StaticTimeAlert.BIWEEKLY_CONTEST, 1), "Added an duplicate serverID to a bucket"
    assert staticTimeBucket.addToBucket(StaticTimeAlert.BIWEEKLY_CONTEST, 2), "Failed to add a valid serverID to bucket"
    assert initialBucket != staticTimeBucket.buckets, "Intial bucket equal to buckets affter an add"
    assert not staticTimeBucket.addToBucket("BADTYPE", 5), "Added with an invalid alert type"

    # ===== TESTING REMOVE FROM BUCKET =====
    assert not staticTimeBucket.removeFromBucket(StaticTimeAlert.BIWEEKLY_CONTEST, -999), "Removed an invalid serverID"
    assert staticTimeBucket.removeFromBucket(StaticTimeAlert.BIWEEKLY_CONTEST, 2), "Failed to remove a valid serverID"
    assert initialBucket == staticTimeBucket.buckets, "Initial bucket not equal to bucket after removing the only thing that was added"
    return True

# contest time bucket
def testContestTimeBucket() -> bool:
    # 15, 30, 60, 120, 360, 720, 1440
    
    # s1 = alerts on, [15, 30]
    # s2 = alerts off, [15, 30, 60, 120]
    # s3 = alerts on, [] 
    
    app = makeApp()
    
    contestTimeBucket = app.contestTimeBucket
    assert contestTimeBucket is not None, "App's contestTimeBucket is None"

    initialBucket = copy.deepcopy(contestTimeBucket.buckets)

    # get bucket test
    # test where i know something should be there
    # test where something shouldnt be
    assert not contestTimeBucket.getBucket(-999), "Got something that should'nt exist"
    assert len(contestTimeBucket.getBucket(1440)) == 0, "A bucket that should exist but be empty had items"

    bucket15min = contestTimeBucket.getBucket(15)
    assert bucket15min, "Failed to get the 15 min bucket, which should exist and have items"

    # servers 1 and 2 both have intervals for bucket 15
    # however, only server 1 has alerts on, so it should be the only thing in
    assert len(bucket15min) == 1, "Bucket did not have exactly 1 item when it should"

    serverInBucket = list(bucket15min)[0] # sets are not subscriptable
    assert serverInBucket == 1, "The only server in the bucket was not the expected server"

    # add bucket
    assert not contestTimeBucket.addToBucket(-999, 1), "Added an invalid interval"
    assert not contestTimeBucket.addToBucket(15, 1), "Added a duplciate SID"
    assert contestTimeBucket.addToBucket(15, 2), "Failed to add a server when it should've passed"
    assert initialBucket != contestTimeBucket.buckets, "Initial bucket is equal to current bucket after adding something"

    # remove bucket
    assert not contestTimeBucket.removeFromBucket(-999, 1), "Removed from an invalid interval"
    assert not contestTimeBucket.removeFromBucket(15, 3), "Removed an ID from a bucket that it should't have"
    assert contestTimeBucket.removeFromBucket(15, 2), "Failed to remove an ID when it shouldn't have"
    assert initialBucket == contestTimeBucket.buckets, "Initial bucket not equal to current buckets after removing the only thing added"

    return True


# problem bucket
def testProblemBucket() -> bool:
    app = makeApp()
    
    problemBucket = app.problemBucket
    assert problemBucket is not None, "App's problemBucket is None"

    # problemBucket.printBucketClean()
    
    return True
