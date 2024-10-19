"""
A file that contains all the constants used in the bot

Attributes:
    URLS - The urls used in the bot
    ImageFolders - The names of the folders in the images director that contain other images
    Times - Relevant static times
    Difficulty - The difficulty of the problems
    Boundaries - Static boundaries for the bot
    DatabaseTables - The names of the database tables
    DatabaseFields - Tuples of the respective fields for the database tables
    Problemset - The CSV filenames for the problemsets
    Query - Query Strings for the leetcode graphql api
"""
from enum import Enum

class URLS(Enum):
    """
    The urls used in the bot. Has:
    - LEETCODE_API: The graphql api for leetcode
    - LEETCODE_PROBLEMS: The url to get all the problems from leetcode json
    - LEETCODE_CONTESTS: The link to the contests page 
    """
    LEETCODE_API = "https://leetcode.com/graphql"
    LEETCODE_PROBLEMS = "https://leetcode.com/api/problems/all/"
    LEETCODE_CONTESTS = "https://leetcode.com/contest/"
    
class ImageFolders(Enum):
    """ 
    The names of the folders in the images director that contain other images. Has:
    - THUMBS_UP: The folder that contains the thumbs up images. e.g. "thumbs_up"
    """
    THUMBS_UP = "thumbs_up"

class Times(Enum):
    """ 
    Relevant static times. Has:
    - OFFICIAL_DAILY_RESET: The time the official daily problem resets e.g. "20:00"
    - CONTEST_TIME_ALERTS: The times to alert for contests. e.g. ["15min", "30min", "1hour", "2hour30min", "6hour", "12hour", "24hour"]
    """
    OFFICIAL_DAILY_RESET = "20:00" # 8 pm est since its where im based, easier for calcs 
    CONTEST_TIME_ALERTS = ["t15min", "t30min", "t1hour", "t2hour30min", "t6hour", "t12hour", "t24hour"]


class Difficulty(Enum):
    """
    The difficulty of the problems. Has:
    - EASY: "Easy"
    - MEDIUM: "Medium"
    - Hard: "Hard"
    - RANDOM: "Random"
    """
    EASY = "Easy"
    MEDIUM = "Medium"
    HARD = "Hard"
    RANDOM = "Random"

class Boundaries(Enum):
    """ 
    Static boundaries for the bot. Has
    - MAX_PROBLEMS: The max amount of problems allowed. e.g. 3
    - MIN_PROBLEMS: The min amount of problems allowed. e.g. 0
    """
    MAX_PROBLEMS = 3
    MIN_PROBLEMS = 0

class DatabaseTables(Enum):
    """ 
    The names of the database tables. Has:
    - PROBLEMS: "problems"
    - USERS: "users"
    - SERVERS: "servers"
    - CONTESTS: "contests"
    - ACTIVE_PROBLEMS: "active_problems"
    """
    PROBLEMS = "problems"
    USERS = "users"
    SERVERS = "servers"
    CONTESTS = "contests"
    ACTIVE_PROBLEMS = "active_problems"

class DatabaseFields(Enum):
    """
    Tuples of the respective fields for the database tables. Has:
    - USERS: ("userID", "leetcodeUsername", "serverID", "weeklyOpt", "biweeklyOpt", "problemsOpt")
    - SERVERS: ("serverID", "channelID", "problemsActive", "weeklyOpt", "biweeklyOpt", "officialDaily", "notifType", "timezone")
    - PROBLEMS: ("serverID", "problemID", "dow", "hour", "difficulty", "premium")
    - CONTESTS: ("serverID", "15min", "30min", "1hour", "2hour30min", "6hour", "12hour", "24hour")
    - ACTIVE_PROBLEMS: ("serverID", "p1", "p2", "p3")
    """
    USERS = ("userID", "leetcodeUsername", "serverID", "weeklyOpt", "biweeklyOpt", "problemsOpt")
    SERVERS = ("serverID", "channelID", "problemsActive", "weeklyOpt", "biweeklyOpt", "officialDaily", "notifType", "timezone")
    PROBLEMS = ("serverID", "problemID", "dow", "hour", "difficulty", "premium")
    CONTESTS = ("serverID", "t15min", "t30min", "t1hour", "t2hour30min", "t6hour", "t12hour", "t24hour")
    ACTIVE_PROBLEMS = ("serverID", "p1", "p2", "p3")

class Problemset(Enum):
    """ 
    The CSV filenames for the problemsets. Has:
    - FREE: "free.csv"
    - PAID: "paid.csv"
    - BOTH: "all.csv"
    """
    FREE = "free.csv"
    PAID = "paid.csv"
    BOTH = "all.csv"

class Query(Enum):
    """ 
    Query Strings for the leetcode graphql api. Has:
    - DAILY_PROBLEM: Retrieves info about the daily problem
    - RECENT_SUBMISSIONS: Retrieves the recent submissions of a user
    - USER_PROFILE: Retrieves the profile of a user
    - QUESTION_INFO: Retrieves the info of a question
    - UPCOMING_CONTESTS: Retrieves the upcoming contests info 
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
    