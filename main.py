from utils.initializer import Initializer

def main():
    app = Initializer.initApp(True)
    app.problemBucket.printBucketClean()
    

if __name__ == "__main__":
    main()
    
# servers = generate()
# servers = readFromFiles()
# dowBucket, staticBucket, contestAlertBucket = setupBuckets(servers)
# cacheManager, queryManager, problemManager, alertManager = setupManagers(servers, dowBucket, staticBucket, contestAlertBucket)

# dowBucket.printBucketClean()  # Print the day of week buckets
# dowBucket.getBucket(1).printBucketClean()  # Print the bucket for day 1

# output = alertManager.handleProblemAlerts(1, 7, 0)  # Example call to handle problem alerts for day 1, hour 2, interval 1
# print(output)

# staticBucket.printBucketClean()  # Print the static buckets

# out = alertManager.collectStaticAlerts("daily")
# print(out)
    
# def changeWhileRunning():
#     servers = readFromFiles()
#     server = servers[1]
#     server.settings.officialDailyAlerts = not server.settings.officialDailyAlerts
#     server.toJSON()  # Save the changes to the server's JSON file

# def testIfBucketHasOldProblemsWhenAdding():
#     DOW = 1
#     SERVERID = 1
#     PROBLEMID =1 
    
#     server = generateTestServers(2)[0] # 2 because range is 1,n and n is not inclusive so it gens 1    
#     server.serverID = SERVERID
#     server.toJSON()        
    
#     servers: dict[int, Server] = dict()
#     servers[server.serverID] = server # add the server to the servers dict
    
#     dowBucket = DowBucket()
#     problemManager = setupProblemManager(servers, dowBucket)
    
#     problems = generateRandomProblems(3)
#     for problem in problems:
#         problem.dow = DOW
#         problem.problemID = PROBLEMID
#         problem.serverID = SERVERID

#     p1, p2, p3 = problems
    
#     x1 = problemManager.addProblem(p1)
#     x2 = problemManager.addProblem(p2)
#     x3 = problemManager.addProblem(p3)    
#     print(x1, x2, x3)
    
#     print(server)
#     dowBucket.getBucket(DOW).printBucketClean()

#     problemManager.removeProblem(p3)
#     print("After removing p1:")
#     print(server)
#     dowBucket.getBucket(DOW).printBucketClean()


    
# MISC LINES, MIGHT BE USEFUL LATER
    
# for problem in generateRandomProblems(100):
    # problemManager.selectProblem(problem)

# problem = generateRandomProblems(1)[0]
# problemSlug = problemManager.selectProblem(problem)
# problemSlug = "two-sum"

# if cacheManager.existsInCache(problemSlug):
#     print("Getting from cache")
#     problemInfo = cacheManager.getFromCache(problemSlug)
# else:
#     print("Performing query")
#     problemInfo = queryManager.performQuery(Query.QUESTION_INFO, {"titleSlug" : problemSlug})
#     cacheManager.cacheProblem(problemInfo)

# print(problemInfo)