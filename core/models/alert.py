from enum import Enum

# simple model to contain an alert
class Alert:
    def __init__(self, type: "AlertType", serverID: int, channelID: int, info: dict):
        self.type = type
        self.serverID = serverID
        self.channelID = channelID
        self.info = info if info else {}
        
class AlertType(Enum):
    PROBLEM = "problem"
    CONTEST_TIME_AWAY = "contest-time-away"
    DAILY_PROBLEM = "daily-problem"
    WEEKLY_CONTEST = "weekly-contest"
    BIWEEKLY_CONTEST = "biweekly-contest"