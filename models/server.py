import os

from models.problem import Problem
from models.server_settings import ServerSettings

from utils import json_helper as jsonh

# representation of a discord server
class Server:
    
    MAXPROBLEMS = 5

    def __init__(self, sid:int, settings:ServerSettings, previousProblems:list[str] = None, activeProblems:list[tuple[str, str, set]] = None):
        self.serverID = sid
        self.settings = settings
        self.previousProblems = previousProblems if previousProblems is not None else []
        self.problems :list[Problem] = [None] * (self.MAXPROBLEMS + 1) # +1 to account for 0 index, so 0 is unused
        self.activeProblems = activeProblems if activeProblems is not None else [("", "", set())] * (self.MAXPROBLEMS + 1)

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
            f"\tactiveProblems=[\n"
            f"\t\t{self.activeProblems}\n"
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
        self.activeProblems[id] = ("", "", set()) # reset the active problem slug as well
        self.toJSON()
        return True

    # adds an active problem which is one users can try and submit to 
    # when a problem is deemed active is is also deemed "previous"
    # TODO: should be being called on the results gotten back from the alert builder
    # and right before being added
    def addActiveProblem(self, slug: str, difficulty: str, problemID: int) -> bool:
        if not self.addPreviousProblem(slug): # to prevent duplicates
            return False

        for problem in self.activeProblems:
            if problem[0] == slug: # get the slug portion of the tuple
                return False
    
        if problemID < 0 or problemID > self.MAXPROBLEMS:
            return False

        # initialize the active problem with an empty set of users
        # because no one has submitted yet
        self.activeProblems[problemID] = (slug, difficulty, set())
        self.toJSON()
        return True

    # adds a problem to the previous problems list
    def addPreviousProblem(self, slug: str) -> None:
        if slug not in self.previousProblems:
            self.previousProblems.append(slug)
            self.toJSON()
            return True
        return False

    def addSubmittedUser(self, userID: int, problemID) -> bool:
        
        print(problemID)
        
        if not self.isProblemIDActive(problemID):
            print("Problem ID is not active")
            return False
        
        
        activeProblem = self.activeProblems[problemID]
        if not activeProblem:
            print("Active problem is empty")
            print(activeProblem)
            return False
        
        submittedUsers: set = activeProblem[2]
        submittedUsers.add(userID)
        self.toJSON() # save
        return True

    def isProblemDuplicate(self, slug: str) -> bool:
        return slug in self.previousProblems
    
    def isProblemIDActive(self, problemID: int) -> bool:
        if problemID < 0 or problemID > self.MAXPROBLEMS:
            return False
        return self.activeProblems[problemID][0] != ""
    
    def resetActiveProblem(self, problemID: int) -> bool:
        if problemID < 0 or problemID > self.MAXPROBLEMS:
            return False
        
        # reset the active problem to an empty tuple
        self.activeProblems[problemID] = ("", "", set())
        self.toJSON()
        return True

    
    # save the server to JSON
    def toJSON(self):
        data = {
            "serverID": self.serverID,
            "settings": self.settings.toJSON(),
            "previousProblems": self.previousProblems,
            "activeProblems": [(slug, difficulty, list(users)) for slug, difficulty, users in self.activeProblems], 
            "problems": [problem.toJSON() for problem in self.problems if problem]
        }
        jsonh.writeJSON(f"{os.path.join('data', 'servers', f'{self.serverID}.json')}", data)
        
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
        activeProblems = [(slug, difficulty, set(users)) for slug, difficulty, users in data["activeProblems"]]

        server = Server(sid, settings, previousProblems, activeProblems)

        for prob in problems:
            pid = prob.problemID
            if prob and (pid > 0) and (pid <= Server.MAXPROBLEMS):
                server.problems[pid] = prob

        return server

