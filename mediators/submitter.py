from pyutils import Clogger

from models.server import Server
from models.user import User
from services.query_service import QueryService

class Submitter:
    def __init__(self, servers: dict[int, Server], users: dict[int, User], queryService: QueryService):
        self.servers = servers
        self.users = users
        self.queryService = queryService
        Clogger.info("Submitter initialized")
    
    # checks if a user has completed problems in the servers active problems
    async def submit(self, serverID: int, userID: int) -> bool:
        if (serverID not in self.servers) or (userID not in self.users):
            return False

        Clogger.info("Processing submission")

        server: Server = self.servers[serverID]
        user: User = self.users[userID]
        
        submissions = await self.queryService.getUserRecentAcceptedSubmissions(user.leetcodeUsername, 15)
        
        # collect the slugs of the problems the user has submitted alongside the submitted users already
        # check if the slugs match, if they do, and the user hasnt submitted, then we can add they points
        
        activeProblems = server.activeProblems
        
        for pid, activeProblem in enumerate(activeProblems):
            slug, difficulty, submittedUsers = activeProblem
            
            # this problem is not active, so we skip it
            if slug == "" or difficulty == "":
                continue

            if not await self.userCompletedProblem(user=user, slug=slug, submissions=submissions):
                Clogger.warn("User has not completed the problem")
                continue
            
            if userID in submittedUsers:
                Clogger.warn("User has already submitted this problem")
                continue

            if not server.addSubmittedUser(user.discordID, pid):
                Clogger.warn("Error adding submitted user")
                continue
            
            # if we get here, the user has completed a new problem
            # server.addSubmittedUser() returns a bool

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
    # can pass in submissions to avoid querying the API
    async def userCompletedProblem(self, user: User, slug: str, submissions: dict = None) -> bool:
        # uses the api to check a users recent submissions returns true if they have
        Clogger.info(f"Checking if user {user.discordID} has completed problem {slug}")
        leetcodeUsername = user.leetcodeUsername
        if not submissions:
            submissions = await self.queryService.getUserRecentAcceptedSubmissions(leetcodeUsername)
            
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
        
