from core.problem import Problem

class Server:
    
    MAXPROBLEMS = 5
    
    def __init__(self, sid, settings):
        self.serverID = sid
        self.settings = settings
        self.problems:list[Problem] = [None] * self.MAXPROBLEMS # index is the problem id
    
    def addProblem(self, problem: Problem) -> bool:
        id:int = problem.problemID
        if id < 0 or id >= self.MAXPROBLEMS:
            return False
        self.problems[id] = problem
        return True
        # add it so the saved files as well
    
    def removeProblem(self, problem: Problem) -> bool:
        id:int = problem.problemID
        if id < 0 or id > self.MAXPROBLEMS:
            return False
        self.problems[id] = None
        # remove it from the saved files as well
        
    def __hash__(self):
        return hash(self.serverID)
    
    def handleProblem(self, problemID:int):
        # this is the main call that "handles" using the observer pattern
        pass
    
    def handleContestAlert(self, timeAway:str):
        # this sends a message to the server telling them how far away the 
        pass

    def toCSV():
        pass
    
    def fromCSV():
        pass