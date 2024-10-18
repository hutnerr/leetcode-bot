from enum import Enum

class DaysOfWeek(Enum):
    SUNDAY = "1"
    MONDAY = "2"
    TUESDAY = "3"
    WEDNESDAY = "4"
    THURSDAY = "5"
    FRIDAY = "6"
    SATURDAY = "7"

class Difficulty(Enum):
    EASY = "1"
    MEDIUM = "2"
    HARD = "3"
    RANDOM = "4"

class Boundaries(Enum):
    MAX_PROBLEMS = 3
    MIN_PROBLEMS = 0

class DatabaseTables(Enum):
    PROBLEMS = "problems"
    USERS = "users"
    SERVERS = "servers"
    CONTESTS = "contests"
    ACTIVE_PROBLEMS = "active_problems"

class DatabaseFields(Enum):
    PROBLEMS = ("serverID", "problemNum", "dow", "hour", "difficulty", "premium")
    USERS = ("userID", "leetcodeUsername", "serverID", "weeklyOpt", "biweeklyOpt", "problemsOpt")
    SERVERS = ("serverID", "channelID", "problems", "weeklyContests", "biweeklyContests", "timezone")
    CONTESTS = ("serverID", "15min", "30min", "1hr", "2hr30min", "6hr", "12hr", "24hr")
    ACTIVE_PROBLEMS = ("serverID", "p1", "p2", "p3")

class Premium(Enum):
    FREE = 1
    PAID = 2
    BOTH = 3

# the csv files of the related problemsets
class Problemset(Enum):
    FREE = "free.csv"
    PAID = "paid.csv"
    BOTH = "all.csv"

# the UTC times the contests occur
class Contests(Enum):
    WEEKLY = "24:00"
    BIWEEKLY = "12:00"

# query strings for the leetcode graphql api
class Query(Enum):
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
    