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
def testStaticTimeBucket() -> tuple[bool, str]:
    app = makeApp()
    
    staticTimeBucket = app.staticTimeBucket
    if not staticTimeBucket:
        return (False, "App's staticTimeBucket is None")
    
    # staticTimeBucket.printBucketClean()
    initialBucket = copy.deepcopy(staticTimeBucket.buckets)
    
    # ===== TESTING GET BUCKET =====
    weeklyBucket = staticTimeBucket.getBucket(StaticTimeAlert.WEEKLY_CONTEST)
    if not weeklyBucket:
        return (False, "Weekly bucket is None")
    
    weeklyExpected = set([1, 3])
    if weeklyBucket != weeklyExpected:
        return (False, "Weekly did not match the expected")
    
    biweeklyBucket = staticTimeBucket.getBucket(StaticTimeAlert.BIWEEKLY_CONTEST)
    if not biweeklyBucket:
        return (False, "Biweekly bucket is None")
    
    biweeklyExpected = set([1])
    if biweeklyBucket != biweeklyExpected:
        return (False, "Biweekly did not match the expected")
    
    dailyBucket = staticTimeBucket.getBucket(StaticTimeAlert.DAILY_PROBLEM)
    if not dailyBucket:
        return (False, "Daily bucket is None")

    dailyExpected = set([1])
    if dailyBucket != dailyExpected:
        return (False, "Daily did not match the expected")
    
    # FOR ADD TO AND REMOVE FROM, USING ALONE WILL MAKE INCONSISTENCIES WITH SERVER INTERALLY
    # USE THE SYNCHRONIZER TO PREVENT IN REAL USE
    
    # ===== TESTING ADD TO BUCKET =====
    if staticTimeBucket.addToBucket(StaticTimeAlert.BIWEEKLY_CONTEST, 1):
        return (False, "Added an duplicate serverID to a bucket")
    
    if not staticTimeBucket.addToBucket(StaticTimeAlert.BIWEEKLY_CONTEST, 2):
        return (False, "Failed to add a valid serverID to bucket")
    
    if initialBucket == staticTimeBucket.buckets:
        return (False, "Intial bucket equal to buckets affter an add")
    
    if staticTimeBucket.addToBucket("BADTYPE", 5):
        return (False, "Added with an invalid alert type")
    
    # ===== TESTING REMOVE FROM BUCKET =====
    
    if staticTimeBucket.removeFromBucket(StaticTimeAlert.BIWEEKLY_CONTEST, -999):
        return (False, "Removed an invalid serverID")
    
    if not staticTimeBucket.removeFromBucket(StaticTimeAlert.BIWEEKLY_CONTEST, 2):
        return (False, "Failed to remove a valid serverID")
    
    if initialBucket != staticTimeBucket.buckets:
        return (False, "Initial bucket not equal to bucket after removing the only thing that was added")

    return (True, "All Good!")

# contest time bucket
def testContestTimeBucket() -> tuple[bool, str]:
    # 15, 30, 60, 120, 360, 720, 1440
    
    # s1 = alerts on, [15, 30]
    # s2 = alerts off, [15, 30, 60, 120]
    # s3 = alerts on, [] 
    
    app = makeApp()
    
    contestTimeBucket = app.contestTimeBucket
    if not contestTimeBucket:
        return (False, "App's contestTimeBucket is None")
    
    initialBucket = copy.deepcopy(contestTimeBucket.buckets)
    
    # get bucket test
    # test where i know something should be there
    # test where something shouldnt be
    if contestTimeBucket.getBucket(-999):
        return (False, "Got something that should'nt exist")
    
    if len(contestTimeBucket.getBucket(1440)) != 0:
        return (False, "A bucket that should exist but be empty had items")
    
    bucket15min = contestTimeBucket.getBucket(15)
    if not bucket15min:
        return (False, "Failed to get the 15 min bucket, which should exist and have items")
    
    # servers 1 and 2 both have intervals for bucket 15
    # however, only server 1 has alerts on, so it should be the only thing in
    if len(bucket15min) != 1:
        return (False, "Bucket did not have exactly 1 item when it should")
    
    serverInBucket = list(bucket15min)[0] # sets are not subscriptable
    if serverInBucket != 1:
        return (False, "The only server in the bucket was not the expected server")
        
    # add bucket
    if contestTimeBucket.addToBucket(-999, 1):
        return (False, "Added an invalid interval")
    
    if contestTimeBucket.addToBucket(15, 1):
        return (False, "Added a duplciate SID")
    
    if not contestTimeBucket.addToBucket(15, 2):
        return (False, "Failed to add a server when it should've passed")
    
    if initialBucket == contestTimeBucket.buckets:
        return (False, "Initial bucket is equal to current bucket after adding something")

    # remove bucket
    if contestTimeBucket.removeFromBucket(-999, 1):
        return (False, "Removed from an invalid interval")
    
    if contestTimeBucket.removeFromBucket(15, 3):
        return (False, "Removed an ID from a bucket that it should't have")
    
    if not contestTimeBucket.removeFromBucket(15, 2):
        return (False, "Failed to remove an ID when it shouldn't have")
    
    if initialBucket != contestTimeBucket.buckets:
        return (False, "Initial bucket not equal to current buckets after removing the only thing added")    
    
    return (True, "All Good!")


# problem bucket
def testProblemBucket() -> tuple[bool, str]:
    app = makeApp()
    
    problemBucket = app.problemBucket
    if not problemBucket:
        return (False, "App's problemBucket is None")
    
    problemBucket.printBucketClean()
    
    
    return (True, "All Good!")




