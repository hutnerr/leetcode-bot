from core.problem import Problem
from core.server_settings import ServerSettings
from utils import json_helper as jsonh

class Server:
    
    MAXPROBLEMS = 5
    
    def __init__(self, sid:int, settings:ServerSettings):
        self.serverID = sid
        self.settings = settings
        self.problems:list[Problem] = [None] * (self.MAXPROBLEMS + 1) # +1 to account for 0 index, so 0 is unused

    def __str__(self) -> str:
        return (f"Server(serverID={self.serverID}, "
                f"settings={self.settings}, "
                f"problems={self.problems})")

    def __repr__(self) -> str:
        return self.__str__()
    
    def addProblem(self, problem: Problem) -> bool:
        id:int = problem.problemID
        if id < 0 or id > self.MAXPROBLEMS:
            return False
        self.problems[id] = problem
        self.toJSON()
        return True
    
    def removeProblem(self, problem: Problem) -> bool:
        id:int = problem.problemID
        if id < 0 or id > self.MAXPROBLEMS:
            return False
        self.problems[id] = None
        self.toJSON()
        return True

    def __hash__(self):
        return hash(self.serverID)
    
    def handleProblem(self, problemID:int):
        # TODO: Implement the logic to handle the problem
        # this is the main call that "handles" using the observer pattern
        print(f"Server {self.serverID} is handling problem {problemID}: {self.problems[problemID]}")
    
    def handleContestAlert(self, timeAway:str):
        # TODO: Implement the logic to handle contest alert
        # this sends a message to the server telling them how far away the 
        pass
    
    # save the server to JSON
    def toJSON(self):
        data = {
            "serverID": self.serverID,
            "settings": self.settings.toJSON(),
            "problems": [problem.toJSON() for problem in self.problems if problem]
        }
        jsonh.writeJSON(f"data/servers/{self.serverID}.json", data)
        

    # ===================================
    # helper functions
    # ===================================
    @staticmethod
    def buildFromJSON(data: dict) -> "Server":
        if data is None:
            print("Error: No data provided to build Server from JSON.")
            return None
        sid = data["serverID"]
        settings = ServerSettings.buildFromJSON()
        problems = [Problem.buildFromJSON(prob) for prob in data["problems"]]

        server = Server(sid, settings)
        
        for prob in problems:
            pid = prob.problemID
            if prob and (pid > 0) and (pid <= Server.MAXPROBLEMS):
                server.problems[pid] = prob

        return server