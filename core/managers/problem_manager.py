from buckets.dow_buckets import DowBucket
from core.server import Server
from core.problem import Problem

class ProblemManager:
    
    def __init__(self, dowBucket: DowBucket):
        self.dowBucket = dowBucket

    def addProblem(problem: Problem, server: Server):
        # check if the problem id i want to add already exists within the server
        # if it does then i know it should already be in a bucket
        # since that is the case, the old problem must be removed from the bucket
        # get the problem to remove and pass it to the dowBucket to remove it
        # once it is remove, we can safely add to the dowBucket and the server
        pass