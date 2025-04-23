from core.problem import Problem
from core.server_settings import ServerSettings
from utils import logger

class Server:
    
    MAXPROBLEMS = 5
    
    def __init__(self, sid:int, settings:ServerSettings):
        self.serverID = sid
        self.settings = settings
        self.problems:list[Problem] = [None] * self.MAXPROBLEMS # index is the problem id
    
    def __str__(self) -> str:
        return f"serverID:{self.serverID}"

    def __repr__(self) -> str:
        return self.__str__()
    
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
        print(f"Server {self.serverID} is handling problem {problemID}: {self.problems[problemID]}")
    
    def handleContestAlert(self, timeAway:str):
        # this sends a message to the server telling them how far away the 
        pass

    def toCSV(self) -> str:
        return f"{self.serverID}"
    
def serverFromCSV(line:str) -> "Server":
    split = line.split(",")
    try:
        return Server(
            int(split[0]), # problem id
            None, # server settings
        )
    except Exception as e:
        logger.error(f"Error reading problem from csv: {line} {e}")
    