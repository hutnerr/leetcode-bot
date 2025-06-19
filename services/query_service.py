import requests
from enum import Enum

# performs queries
class QueryService:
    API_URL: str = "https://leetcode.com/graphql"
    
    # gets the official daily leetcode problem
    def getDailyProblem(self) -> dict:
        args = {} 
        return self._performQuery(QueryStrings.DAILY_PROBLEM, args)
    
    # can define an amount to get only that many
    def getUserRecentAcceptedSubmissions(self, username: str, amount: int = 10) -> dict:
        args = {
            "username" : username,
            "limit" : amount
        }
        return self._performQuery(QueryStrings.RECENT_SUBMISSIONS, args)
    
    def getUserProfile(self, username: str) -> dict:
        args = {
            "username" : username
            }
        return self._performQuery(QueryStrings.USER_PROFILE, args)
    
    def getUserProblemsSolved(self, username: str) -> dict:
        args = {
            "username" : username
        }
        return self._performQuery(QueryStrings.USER_PROBLEMS_SOLVED, args)
    
    def getQuestionInfo(self, slug: str) -> dict:
        args = {
            "titleSlug" : slug
        }
        return self._performQuery(QueryStrings.QUESTION_INFO, args)
    
    def getUpcomingContests(self) -> dict:
        args = {}
        return self._performQuery(QueryStrings.UPCOMING_CONTESTS, args)

    # internal query actions
    def _performQuery(self, query: str, variables: dict) -> dict:
        json = {
            'query': query.value,
            'variables': variables
        }
        return requests.post(self.API_URL, json=json).json()

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
    
    # TODO: Write tests for this query
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
