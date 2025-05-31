import os
import random

from core.buckets.dow_buckets import DowBucket

from core.server import Server
from core.problem import Problem

class ProblemManager:
    
    def __init__(self, servers: dict[int, Server], dowBucket: DowBucket):
        self.servers = servers
        self.dowBucket = dowBucket
        self.problemSets = { # memory is cheap!
            "free": {
                "easy" : [],
                "medium" : [],
                "hard" : []
                },
            "paid": {
                "easy" : [],
                "medium" : [],
                "hard" : []
                },
            "all": {
                "easy" : [],
                "medium" : [],
                "hard" : []
            }
        }
        self.setupManager()

    def setupManager(self):
        # read in the problemsets into memory for faster access
        PROBLEMSETPATH = os.path.join("data", "problems.csv")
        with open(PROBLEMSETPATH, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            for line in lines:
                slug, dif, paid = line.strip().lower().split(",")
                
                self.problemSets["all"][dif].append(slug) # always add to all 
                
                # add to paid/free conditionally
                if paid == "true": 
                    self.problemSets["paid"][dif].append(slug)
                else:
                    self.problemSets["free"][dif].append(slug)

    # called if the csv problemset is updated
    def refreshProblemSets(self):
        self.problemSets = {
            "free": [],
            "paid": [],
            "all": []
        }
        self.setupManager()

    # adds a problem to where it belongs. ie the server and proper bucket
    def addProblem(self, problem: Problem):
        pid = problem.problemID
        sid = problem.serverID

        server = self.servers[sid]
        
        # we have a problem with this id already, thus we need to remove it
        if server.problems[pid] is not None:
            problemToRemove = server.problems[pid]
            if not self.dowBucket.removeFromBucket(problemToRemove):
                print("Failed to remove from bucket")
                return False
        
        # we either didn't have a problem to remove, or did and we removed it
        # we can safely add to the server and the buckets now
        if not server.addProblem(problem):
            print("Failed to add problem")
            return False
        
        if not self.dowBucket.addToBucket(problem):
            print("Failed to add to bucket")
            return False
        
        return True

    # removes a problem from the server and the bucket
    def removeProblem(self, problem: Problem):
        pid = problem.problemID
        sid = problem.serverID

        server = self.servers[sid]
        
        # we have a problem with this id already, thus we need to remove it
        if server.problems[pid] is None:
            print("No problem to remove")
            return False

        if not server.removeProblem(problem):
            print("Failed to remove problem from server")
            return False
        
        if not self.dowBucket.removeFromBucket(problem):
            print("Failed to remove from bucket")
            return False
        
        return True
    
    # uses the problem to get a slug for the problem
    def selectProblem(self, problem: Problem) -> str:
        match problem.premium:
            case 0: # free
                ps = self.problemSets["free"]
            case 1: # paid
                ps = self.problemSets["paid"]
            case 2: # all
                ps = self.problemSets["all"]
            case _: 
                return None
            
        difficulty = random.choice(problem.difficulties)        
        slug = random.choice(ps[difficulty])
        return slug
        