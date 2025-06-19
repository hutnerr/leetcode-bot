import copy
import random
from testing.generator import GeneratedServers
from utils.initializer import Initializer
from models.app import App
from models.problem import Problem
from models.user import User
from models.alert import Alert, AlertType
from buckets.static_time_bucket import StaticTimeAlert

# mediator integration testing
def makeApp() -> App:
    servers = GeneratedServers().collectServers()
    return Initializer.initApp(passedInServers=servers)


def testAlertBuilder() -> bool:
    INVALIDNUM = -999
    
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
    # - 5 problems: all dow=1, hour=1, interval=1. 
    # - really is 1 problem because it has the same pid so it gets overwritten
    
    # test for buckets that SHOULD have stuff in them, and then for buckets that
    # i know will NOT have anything in them
        
    # TEST BUILD PROBLEM ALERTS
    assert len(alertBuilder.buildProblemAlerts(dow=INVALIDNUM, hour=1, interval=1)) == 0, "Invalid dow should return empty list"
    assert len(alertBuilder.buildProblemAlerts(dow=1, hour=INVALIDNUM, interval=1)) == 0, "Invalid hour should return empty list"
    assert len(alertBuilder.buildProblemAlerts(dow=1, hour=1, interval=INVALIDNUM)) == 0, "Invalid interval should return empty list"

    alerts: Alert = alertBuilder.buildProblemAlerts(dow=1, hour=1, interval=1)
    assert alerts is not None, "Alerts should not be None for valid dow, hour, interval"
    assert len(alerts) == 4, "There should be 4 alerts for the problems in this bucket"
    
    for alert in alerts:
        assert "slug" in alert.info, "Alert info should contain 'slug'"
        assert alert.type == AlertType.PROBLEM, "Alert type should be PROBLEM"
    
    alerts = alertBuilder.buildProblemAlerts(dow=1, hour=1, interval=3) # this should be empty
    assert len(alerts) == 0, "There should be no alerts for this bucket (dow=1, hour=1, interval=3)"

    # TEST BUILD CONTEST ALERTS
    # 15, 30, 60, 120, 360, 720, 1440
    assert len(alertBuilder.buildContestAlerts(15, AlertType.WEEKLY_CONTEST)) == 1, "Should only be 1 alert at this time"
    assert len(alertBuilder.buildContestAlerts(30, AlertType.WEEKLY_CONTEST)) == 1, "Should only be 1 alert at this time"
    assert len(alertBuilder.buildContestAlerts(60, AlertType.WEEKLY_CONTEST)) == 0, "Should be no alerts at this time"

    alerts = alertBuilder.buildContestAlerts(15, AlertType.WEEKLY_CONTEST)
    assert alerts is not None, "Alerts should not be None for valid interval"
    assert len(alerts) == 1, "There should be 1 alert for the weekly contest at this time"
    for alert in alerts:
        assert alert.type == AlertType.WEEKLY_CONTEST, "Alert type should be WEEKLY_CONTEST"
        assert "alertString" in alert.info, "Alert info should contain 'alertString'"

    # TEST BUILD STATIC ALERTS 
    app.staticTimeBucket.removeFromBucket(StaticTimeAlert.DAILY_PROBLEM, 1) # remove from bucket for easier testing
    # after above, weekly should have {1, 3}, biweekly {1}, and daily {}
    
    weekyStaticAlerts = alertBuilder.buildStaticAlerts(StaticTimeAlert.WEEKLY_CONTEST)
    assert weekyStaticAlerts is not None, "Weekly static alerts should not be None"
    assert len(weekyStaticAlerts) == 2, "There should be 2 weekly static alerts"
    
    for alert in weekyStaticAlerts:
        assert alert.type == AlertType.WEEKLY_CONTEST, "Alert type should be WEEKLY_CONTEST"
        assert "alertString" in alert.info, "Alert info should contain 'alertString'"
    
    biweekyStaticAlerts = alertBuilder.buildStaticAlerts(StaticTimeAlert.BIWEEKLY_CONTEST)
    assert biweekyStaticAlerts is not None, "Biweekly static alerts should not be None"
    assert len(biweekyStaticAlerts) == 1, "There should be 1 biweekly static alert"
    # NOTE: This might fail sometimes because the new contest is being returned 
    # in the api query, so it might return false and the length will be 0
    
    
    dailyStaticAlerts = alertBuilder.buildStaticAlerts(StaticTimeAlert.DAILY_PROBLEM)    
    assert dailyStaticAlerts is not None, "Daily static alerts should not be None"
    assert len(dailyStaticAlerts) == 0, "There should be no daily static alerts"
    
    return True

# the synchronizer is responsible for synchronizing the servers with the buckets
# ie making sure they contain the same problems, intervals, and alerts
def testSynchronizer() -> bool:
    INVALIDNUM = -999
    
    app = makeApp()
    synchronizer = app.synchronizer
    assert synchronizer is not None, "App's synchronizer was None"
    
    servers = app.servers
    assert len(servers) == 3, "There should be 3 servers in the app"
    
    server1 = servers[1] # use for testing contest time intervals
    server2 = servers[2] # use for testing problems
    server3 = servers[3] # use for teching static alerts and contest time intervals

    assert server1 is not None, "Server 1 should not be None"
    assert server2 is not None, "Server 2 should not be None"
    assert server3 is not None, "Server 3 should not be None"

    # add problem
    # adding a problem to a server that has a full 5 problems
    validProblem = Problem(pid=1, sid=3, difs="easy", dow=1, hour=1, interval=1, premium=0)
    invalidDOW = Problem(pid=1, sid=1, difs="", dow=INVALIDNUM, hour=1, interval=1, premium=0)
    invalidHour = Problem(pid=1, sid=1, difs="", dow=1, hour=INVALIDNUM, interval=1, premium=0)
    invalidInterval = Problem(pid=1, sid=1, difs="", dow=1, hour=1, interval=INVALIDNUM, premium=0)
    invalidPIDLT0 = Problem(pid=INVALIDNUM, sid=1, difs="", dow=1, hour=1, interval=1, premium=0) # < 0 problem id
    invalidPIDGTMP = Problem(pid=-INVALIDNUM, sid=1, difs="", dow=1, hour=1, interval=1, premium=0) # > server.maxproblems id
    
    # TESTING ADD PROBLEMS
    assert not synchronizer.addProblem(problem=invalidDOW), "Added a problem with an invalid DOW"
    assert not synchronizer.addProblem(problem=invalidHour), "Added a problem with an invalid hour"
    assert not synchronizer.addProblem(problem=invalidInterval), "Added a problem with an invalid interval"
    assert not synchronizer.addProblem(problem=invalidPIDLT0), "Added a problem with a < 0 problem id"
    assert not synchronizer.addProblem(problem=invalidPIDGTMP), "Added a problem with a > server.maxproblems id"
    assert synchronizer.addProblem(problem=validProblem), "Failed to add a valid problem to the server"
    
    assert validProblem in server3.problems, "Problem was not added to the server's problems"
    assert validProblem.getKey() in app.problemBucket.getBucket(dow=1, hour=1, interval=1), "Problem was not added to the problem bucket"
    assert len([problem for problem in server3.problems if problem is not None]) == 1, "Server should have 1 problem because we kept overwriting the same problem id"

    # remove problem
    assert not synchronizer.removeProblem(problem=invalidDOW), "Removed a problem with an invalid DOW"
    assert not synchronizer.removeProblem(problem=invalidHour), "Removed a problem with an invalid hour"
    assert not synchronizer.removeProblem(problem=invalidInterval), "Removed a problem with an invalid interval"
    assert not synchronizer.removeProblem(problem=invalidPIDLT0), "Removed a problem with a < 0 problem id"
    assert not synchronizer.removeProblem(problem=invalidPIDGTMP), "Removed a problem with a > server.maxproblems id"
    
    assert synchronizer.removeProblem(problem=validProblem), "Failed to remove a valid problem from the server"
    assert validProblem.getKey() not in app.problemBucket.getBucket(dow=1, hour=1, interval=1), "Problem was not removed from the problem bucket"
    assert validProblem not in server3.problems, "Problem was not removed from the server's problems"

    # change intervals
    newIntervals = [15, 30, 60, 120]
    invalidIntervals = [INVALIDNUM, -1, 0, 1000]  # invalid intervals
        
    assert not synchronizer.changeAlertIntervals(serverID=INVALIDNUM, newIntervals=newIntervals), "Changed intervals for an invalid server ID"
    assert not synchronizer.changeAlertIntervals(serverID=1, newIntervals=invalidIntervals), "Changed intervals with invalid intervals"
    assert synchronizer.changeAlertIntervals(serverID=3, newIntervals=newIntervals), "Failed to change contest time intervals for server 3"
    assert set(server3.settings.contestTimeIntervals) == set(newIntervals), "Server 3's contest time intervals were not updated correctly"

    # iterate over the bucket and make sure the server3 intervals are in there
    for interval in newIntervals:
        assert server3.serverID in app.contestTimeBucket.getBucket(interval=interval), f"Server 3's ID not found in contest time bucket for interval {interval}"
        
    # iterate over the bucket and make sure the server1 intervals are STILL in there
    for interval in [15, 30]:
        assert server1.serverID in app.contestTimeBucket.getBucket(interval=interval), f"Server 1's ID not found in contest time bucket for interval {interval}"
    
    assert len(app.contestTimeBucket.getBucket(interval=15)) == 2, "15 min bucket should have 2 servers"
    assert len(app.contestTimeBucket.getBucket(interval=30)) == 2, "30 min bucket should have 2 servers"
    assert len(app.contestTimeBucket.getBucket(interval=60)) == 1, "60 min bucket should have 1 server"
    assert len(app.contestTimeBucket.getBucket(interval=120)) == 1, "120 min bucket should have 1 server"

    # change contest alert participation
    # if we're not participating, the server should not be in the bucket
    assert not synchronizer.changeContestAlertParticpation(serverID=INVALIDNUM, participate=False), "Changed contest participation for an invalid server ID"
    assert synchronizer.changeContestAlertParticpation(serverID=1, participate=False), "Failed to change contest participation for server 1"
    assert server1.settings.contestTimeAlerts is False, "Server 1's contest time alerts were not updated correctly"
    assert synchronizer.changeContestAlertParticpation(serverID=3, participate=False), "Failed to change contest participation for server 3"
    assert server3.settings.contestTimeAlerts is False, "Server 3's contest time alerts were not updated correctly"
    # check that the server is not in the bucket anymore
    assert server1.serverID not in app.contestTimeBucket.getBucket(interval=15), "Server 1's ID found in contest time bucket for interval 15"
    assert server3.serverID not in app.contestTimeBucket.getBucket(interval=15), "Server 3's ID found in contest time bucket for interval 15"
    
    # turn back on contest time alerts
    assert synchronizer.changeContestAlertParticpation(serverID=1, participate=True), "Failed to change contest participation for server 1"
    assert server1.settings.contestTimeAlerts is True, "Server 1's contest time alerts were not updated correctly"
    assert synchronizer.changeContestAlertParticpation(serverID=3, participate=True), "Failed to change contest participation for server 3"
    assert server3.settings.contestTimeAlerts is True, "Server 3's contest time alerts were not updated correctly"
    # check that the server is back in the bucket
    assert server1.serverID in app.contestTimeBucket.getBucket(interval=15), "Server 1's ID not found in contest time bucket for interval 15"
    assert server3.serverID in app.contestTimeBucket.getBucket(interval=15), "Server 3's ID not found in contest time bucket for interval 15"
    assert len(app.contestTimeBucket.getBucket(interval=15)) == 2, "15 min bucket should have 2 servers after re-adding"

    # change static alert
    # STATIC ALERT CHANGE TESTING
    assert synchronizer.changeStaticAlert(serverID=1, alert=StaticTimeAlert.WEEKLY_CONTEST, participate=False), "Failed to change weekly contest participation for server 1"
    assert server1.settings.weeklyContestAlerts is False, "Server 1's weekly contest alerts were not updated correctly"
    
    assert synchronizer.changeStaticAlert(serverID=2, alert=StaticTimeAlert.BIWEEKLY_CONTEST, participate=True), "Failed to change biweekly contest participation for server 2"
    assert server2.settings.biweeklyContestAlerts is True, "Server 2's biweekly contest alerts were not updated correctly"
    
    assert synchronizer.changeStaticAlert(serverID=3, alert=StaticTimeAlert.DAILY_PROBLEM, participate=False), "Failed to change daily problem participation for server 3"
    assert server3.settings.officialDailyAlerts is False, "Server 3's official daily alerts were not updated correctly"
    # check that the server is not in the bucket anymore
    assert server1.serverID not in app.staticTimeBucket.getBucket(StaticTimeAlert.WEEKLY_CONTEST), "Server 1's ID found in static time bucket for weekly contest"
    assert server2.serverID in app.staticTimeBucket.getBucket(StaticTimeAlert.BIWEEKLY_CONTEST), "Server 2's ID not found in static time bucket for biweekly contest"
    assert server3.serverID not in app.staticTimeBucket.getBucket(StaticTimeAlert.DAILY_PROBLEM), "Server 3's ID found in static time bucket for daily problem"

    # turn back on static alerts
    assert synchronizer.changeStaticAlert(serverID=1, alert=StaticTimeAlert.WEEKLY_CONTEST, participate=True), "Failed to change weekly contest participation for server 1"
    assert server1.settings.weeklyContestAlerts is True, "Server 1's weekly contest alerts were not updated correctly"
    
    assert synchronizer.changeStaticAlert(serverID=3, alert=StaticTimeAlert.DAILY_PROBLEM, participate=True), "Failed to change daily problem participation for server 3"
    assert server3.settings.officialDailyAlerts is True, "Server 3's official daily alerts were not updated correctly"
    
    # check that the server is back in the bucket
    assert server1.serverID in app.staticTimeBucket.getBucket(StaticTimeAlert.WEEKLY_CONTEST), "Server 1's ID not found in static time bucket for weekly contest"
    assert server2.serverID in app.staticTimeBucket.getBucket(StaticTimeAlert.BIWEEKLY_CONTEST), "Server 2's ID not found in static time bucket for biweekly contest"
    assert server3.serverID in app.staticTimeBucket.getBucket(StaticTimeAlert.DAILY_PROBLEM), "Server 3's ID not found in static time bucket for daily problem"

    return True

def testSubmitter() -> bool:
    app = makeApp()
    submitter = app.submitter
    assert submitter is not None, "App's submitter was None"
    
    users: dict[int, User] = app.users
    user: User = random.choice(list(users.values()))  # pick a random user from the app
    assert user is not None, "User should not be None"
    
    baduser = -9999999999  # invalid user id
    assert user.discordID in users, "User should be in the app's users"
    assert baduser not in users, "Bad user should not be in the app's users"
    
    # get my username and one of the problems ive recently solved at this time
    username = "hutnerr"
    user.leetcodeUsername = username
    
    slug = "maximum-difference-by-remapping-a-digit"
    badslug = "invalid-slug"  # slug that does not exist

    # userCompletedProblem
    assert submitter.userCompletedProblem(user, slug), "User should have completed the problem"
    assert not submitter.userCompletedProblem(user, badslug), "User should not have completed the problem with an invalid slug"

    badusername = "invalid-username12345"
    user.leetcodeUsername = badusername
    assert not submitter.userCompletedProblem(user, slug), "User should not have completed the problem with an invalid username"
    
    user.leetcodeUsername = username # reset username back to a valid one
    
    
    
    # submit
    serverID = 1
    server = app.servers.get(serverID)
    assert server is not None, "Server should not be None"
    
    problemID = 1
    slug = "smallest-even-multiple"    
    server.addActiveProblem(slug, "easy", problemID)  
    
    hardSlug = "median-of-two-sorted-arrays"
    hardProblemID = 2
    server.addActiveProblem(hardSlug, "hard", hardProblemID) 

    dupProblemID = 3
    dupSlug = "two-sum"  # the slug for the problem we want to submit
    server.addActiveProblem(dupSlug, "easy", dupProblemID) # try and add a previous problem to the server
    assert not server.addActiveProblem(dupSlug, "easy", dupProblemID), f"Should not be able to add active problem {dupSlug} as it is a duplicate"
    
    beforePoints = user.points
    assert user.discordID not in server.activeProblems[problemID][2], "User should not be in the submitted users for the problem"
    assert submitter.submit(serverID, user.discordID, problemID), "User should be able to submit the problem"
    assert not submitter.submit(serverID, user.discordID, problemID), "User should not be able to submit the problem again"
    assert user.discordID in server.activeProblems[problemID][2], "User should now be in the submitted users for the problem"
    assert user.points == beforePoints + 1, "User should have 1 point after submitting an easy problem"
    
    assert not submitter.submit(serverID, baduser, problemID), "User should not be able to submit with an invalid user ID"
    assert not submitter.submit(serverID, user.discordID, -1), "User should not be able to submit with an invalid problem ID"
    assert not submitter.submit(serverID, user.discordID, 999999), "User should not be able to submit with a problem ID that does not exist"
    assert not submitter.submit(serverID, user.discordID, hardProblemID), "User should not be able to submit a problem they have not completed"
    assert not submitter.submit(serverID, user.discordID, 4), "User should not be able to submit a problem that is not active "

    return True