from models.server import Server
from models.user import User
from services.query_service import QueryService

class Submitter:
    def __init__(self, servers: dict[int, Server], users: dict[int, User], queryService: QueryService):
        self.servers = servers
        self.users = users
        self.queryService = queryService
    
    # checks if a user has completed problems in the servers active problems
    def submit(self, serverID: int, userID: int) -> bool:
        if (serverID not in self.servers) or (userID not in self.users):
            return False

        server: Server = self.servers[serverID]
        user: User = self.users[userID]
        
        submissions = self.queryService.getUserRecentAcceptedSubmissions(user.leetcodeUsername, 15)
        
        for problem in server.problems:
            problemID = problem.problemID
            
            if not problem:
                return False    
        
            if not server.isProblemIDActive(problemID):
                # print(f"ProblemID {problemID} is not active for server {serverID}")
                return False
            
            activeProblem = server.activeProblems[problemID]
            if not activeProblem:
                # print(f"Active problem not found for problemID {problemID} on server {serverID}")
                return False
            
            slug, difficulty, submittedUsers = activeProblem
            if userID in submittedUsers:
                # user has already submitted this problem
                # print(f"User {userID} has already submitted problem {problemID} on server {serverID}")
                # pass onto the next problem
                continue

            if not self.userCompletedProblem(user, slug, submissions):
                # print(f"User {userID} has not completed problem {slug} on LeetCode")
                return False
            
            if not server.addSubmittedUser(user.discordID, problemID):
                # print(f"Failed to add user {userID} to submitted users for problem {problemID} on server {serverID}")
                return False
            
            match difficulty:
                case "easy":
                    points = 1
                case "medium":
                    points = 3
                case "hard":
                    points = 6
                case _:
                    # print(f"Invalid difficulty {difficulty} for problem {problemID} on server {serverID}")
                    return False
            
            user.addPoints(points)
        return True
    

    # checks if a user has submitted a problem
    # can pass in submissions to avoid querying the API
    def userCompletedProblem(self, user: User, slug: str, submissions: dict = None) -> bool:
        # uses the api to check a users recent submissions returns true if they have
        leetcodeUsername = user.leetcodeUsername
        if not submissions:
            submissions = self.queryService.getUserRecentSubmissions(leetcodeUsername)
        if not submissions or "data" not in submissions:
            return False

        submissions = submissions["data"]["recentAcSubmissionList"]
        slugs = []
        for submission in submissions: # collect all slugs
            if "titleSlug" in submission:
                slugs.append(submission["titleSlug"])
        
        if len(slugs) == 0:
            return False
        
        return slug in slugs
        
