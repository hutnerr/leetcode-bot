from models.server import Server
from models.user import User
from services.query_service import QueryService

class Submitter:
    def __init__(self, servers: dict[int, Server], users: dict[int, User], queryService: QueryService):
        self.servers = servers
        self.users = users
        self.queryService = queryService
    
    # allows a user to submit a problem
    def submit(self, serverID: int, userID: int, problemID: int, queryService: QueryService) -> bool:
        if (serverID not in self.servers) or (userID not in self.users):
            return False
        
        server: Server = self.servers[serverID]
        user: User = self.users[userID]
        
        problem = server.problems[problemID]
        if not problem:
            return False
        
        if problemID not in server.activeProblems:
            return False
        
        activeProblem = server.activeProblems[problemID]
        if not activeProblem:
            return False
        
        slug, difficulty, submittedUsers = activeProblem
        if userID in submittedUsers:
            # user has already submitted this problem
            return False

        if not self.userCompletedProblem(user, slug):
            return False
        
        if not server.addSubmittedUser(user.discordID, problemID):
            return False
        
        match difficulty:
            case "easy":
                points = 1
            case "medium":
                points = 3
            case "hard":
                points = 6
            case _:
                return False
        
        user.addPoints(points)
        return True
    

    # checks if a user has submitted a problem
    def userCompletedProblem(self, user: User, slug: str) -> bool:
        # uses the api to check a users recent submissions returns true if they have
        leetcodeUsername = user.leetcodeUsername
        info = self.queryService.getUserRecentAcceptedSubmissions(leetcodeUsername)
        if not info or "data" not in info:
            return False
        
        submissions = info["data"]["recentAcSubmissionList"]
        slugs = []
        for submission in submissions:
            if "titleSlug" in submission:
                slugs.append(submission["titleSlug"])
        
        if len(slugs) == 0:
            return False
        
        return slug in slugs
        
