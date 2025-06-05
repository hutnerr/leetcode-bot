from enum import Enum
import requests


class QueryManager:
    API_URL: str = "https://leetcode.com/graphql"
    
    def getDailyProblem(self) -> dict:
        args = {} 
        return self.performQuery(Query.DAILY_PROBLEM, args)
    
    def getUserRecentAcceptedSubmissions(self, username: str, amount: int = 10) -> dict:
        args = {
            "username" : username,
            "limit" : amount
        }
        return self.performQuery(Query.RECENT_SUBMISSIONS, args)
    
    def getUserProfile(self, username: str) -> dict:
        args = {
            "username" : username
            }
        return self.performQuery(Query.USER_PROFILE, args)
    
    def getQuestionInfo(self, slug: str) -> dict:
        args = {
            "titleSlug" : slug
        }
        return self.performQuery(Query.QUESTION_INFO, args)
    
    def getUpcomingContests(self) -> dict:
        args = {}
        return self.performQuery(Query.UPCOMING_CONTESTS, args)

    def performQuery(self, query: str, variables: dict) -> dict:
        """
        Perform a query on the leetcode graphql api
        Args:
            query (str): The query to perform. Use tools.consts.Query for the queries
            variables (dict): THe variables to pass to the query
        Returns:
            dict: The json response dict. 
        """
        query = query.value

        json = {
            'query': query,
            'variables': variables
        }
        response = requests.post(self.API_URL, json=json)
        return response.json()


class Query(Enum):
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
