from models.problem import Problem
from models.server_settings import ServerSettings

from utils import json_helper as jsonh

# representation of a discord server
class Server:
    
    MAXPROBLEMS = 5
    
    def __init__(self, sid:int, settings:ServerSettings, previousProblems:list[str] = None):
        self.serverID = sid
        self.settings = settings
        self.previousProblems = previousProblems if previousProblems is not None else []
        self.problems:list[Problem] = [None] * (self.MAXPROBLEMS + 1) # +1 to account for 0 index, so 0 is unused

    def __str__(self) -> str:
        problems_str = ""
        for i, problem in enumerate(self.problems):
            if problem:
                problems_str += f"\t\t[{i}]: {problem}\n"
        return (
            f"Server(\n"
            f"\tserverID={self.serverID},\n"
            f"\tsettings=[\n\t\t{self.settings}\t]\n"
            f"\tpreviousProblems={self.previousProblems},\n"
            f"\tproblems=[\n{problems_str}\t]\n"
            f")"
        )

    def __repr__(self) -> str:
        return self.__str__()
    
    def __hash__(self):
        return hash(self.serverID)
    
    # ADDING AND REMOVING SHOULD BE CALLED BY A SYNCRONIZER
    # TO ENSURE THAT THE BUCKET AND MODEL CONTAIN THE SAME DATA
    def addProblem(self, problem: Problem) -> bool:
        id:int = problem.problemID
        if id < 0 or id > self.MAXPROBLEMS:
            return False
        self.problems[id] = problem
        self.toJSON()
        return True
    
    # ADDING AND REMOVING SHOULD BE CALLED BY A SYNCRONIZER
    # TO ENSURE THAT THE BUCKET AND MODEL CONTAIN THE SAME DATA
    def removeProblem(self, problem: Problem) -> bool:
        id:int = problem.problemID
        if id < 0 or id > self.MAXPROBLEMS:
            return False
        self.problems[id] = None
        self.toJSON()
        return True

    def isProblemDuplicate(self, slug: str) -> bool:
        return slug in self.previousProblems
        
    # adds a problem to the previous problems list
    def addPreviousProblem(self, slug: str):
        if slug not in self.previousProblems:
            self.previousProblems.append(slug)
            self.toJSON()
    
    # save the server to JSON
    def toJSON(self):
        data = {
            "serverID": self.serverID,
            "settings": self.settings.toJSON(),
            "previousProblems": self.previousProblems,
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
        settings = data["settings"]
        settings = ServerSettings.buildFromJSON(settings)
        problems = [Problem.buildFromJSON(prob) for prob in data["problems"]]
        previousProblems = data["previousProblems"]

        server = Server(sid, settings, previousProblems)

        for prob in problems:
            pid = prob.problemID
            if prob and (pid > 0) and (pid <= Server.MAXPROBLEMS):
                server.problems[pid] = prob

        return server
    
