import os
import random

from utils import csv_helper as csvh
from models.problem import Problem

# performs to service of determining a concrete problem based on problem settings
# also acts as a data container for all of the problems
class ProblemService:
    
    def __init__(self):
        self.problemSets = {}
        self.initProblemSets()
        
    # can be used to reset the problemsets
    # should be used if the csv is updated
    def initProblemSets(self):
        self.problemSets = {
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
        lines = csvh.readFromCSV(PROBLEMSETPATH) # returns each line as a list already split
        for line in lines:
            slug, dif, paid = map(str.lower, line) # lowercase each element
            
            self.problemSets["all"][dif].append(slug) # always add to all 
            
            # add to paid/free conditionally
            if paid == "true": 
                self.problemSets["paid"][dif].append(slug)
            else:
                self.problemSets["free"][dif].append(slug)
    
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
        
        if not problem.difficulties:
            return None
        
        difficulty = random.choice(problem.difficulties)        
        slug = random.choice(ps[difficulty])
        return slug
        