import requests
import aiohttp
from enum import Enum

# performs queries
class QueryService:
    API_URL: str = "https://leetcode.com/graphql"
    
    # internal query actions
    def _performRequestsQuery(self, query: str, variables: dict) -> dict:
        json = {
            'query': query.value,
            'variables': variables
        }
        return requests.post(self.API_URL, json=json).json()
    
    async def _performQuery(self, query: str, variables: dict) -> dict:
        json_data = {
            'query': query.value,
            'variables': variables
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(self.API_URL, json=json_data) as resp:
                return await resp.json()

    # gets the official daily leetcode problem
    async def getDailyProblem(self) -> dict:
        args = {} 
        return await self._performQuery(QueryStrings.DAILY_PROBLEM, args)
    
    # can define an amount to get only that many
    async def getUserRecentAcceptedSubmissions(self, username: str, amount: int = 10) -> dict:
        args = {
            "username" : username,
            "limit" : amount
        }
        return await self._performQuery(QueryStrings.RECENT_SUBMISSIONS, args)

    async def getUserProfile(self, username: str) -> dict:
        args = {
            "username" : username
        }
        return await self._performQuery(QueryStrings.USER_PROFILE, args)

    def getUserProfileRequests(self, username: str) -> dict:
        args = {
            "username" : username
        }
        return self._performRequestsQuery(QueryStrings.USER_PROFILE, args)

    async def getUserProblemsSolved(self, username: str) -> dict:
        args = {
            "username" : username
        }
        return await self._performQuery(QueryStrings.USER_PROBLEMS_SOLVED, args)

    async def getQuestionInfo(self, slug: str) -> dict:
        args = {
            "titleSlug" : slug
        }
        return await self._performQuery(QueryStrings.QUESTION_INFO, args)

    async def getUpcomingContests(self) -> dict:
        args = {}
        return await self._performQuery(QueryStrings.UPCOMING_CONTESTS, args)


# enum class that holds the query strings 
# can also be used to see what you need to pass
# and what you will get back
class QueryStrings(Enum):
    """ 
    DAILY_PROBLEM: Retrieves info about the daily problem
    RECENT_SUBMISSIONS: Retrieves the recent submissions of a user
    USER_PROFILE: Retrieves the profile of a user
    QUESTION_INFO: Retrieves the info of a question
    UPCOMING_CONTESTS: Retrieves the upcoming contests info 
    """

    DAILY_PROBLEM = """
    query daily {
        challenge: activeDailyCodingChallengeQuestion {
            question {
                titleSlug
            }
        }
    }
    """

    RECENT_SUBMISSIONS = """
    query recentAcSubmissions($username: String!, $limit: Int!) {
        recentAcSubmissionList(username: $username, limit: $limit) {
            id
            title
            titleSlug
            timestamp
        }
    }
    """

    USER_PROFILE = """
    query getUserProfile($username: String!) {
        matchedUser(username: $username) {
            username
            profile {
                realName
                aboutMe
                userAvatar
                reputation
                ranking
            }
        }
    }
    """
    
    USER_PROBLEMS_SOLVED = """
    query userProblemsSolved($username: String!) {
        matchedUser(username: $username) {
            submitStatsGlobal {
            acSubmissionNum {
                difficulty
                count
                }
            }
        }
    }
    """

    QUESTION_INFO = """
    query questionInfo($titleSlug: String!) {
            question(titleSlug: $titleSlug) {
                questionFrontendId
                title
                difficulty
                content
                likes
                dislikes
                stats
                isPaidOnly
            }
        }
    """

    UPCOMING_CONTESTS = """
    query upcomingContests {
        upcomingContests {
            title
            titleSlug
            startTime
            duration
            __typename
        }
    }
    """
