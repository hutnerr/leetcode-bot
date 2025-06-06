from enum import Enum

# simple model to contain an alert
class Alert:
    def __init__(self, type: "AlertType", serverID: int, channelID: int, info: dict):
        self.type = type
        self.serverID = serverID
        self.channelID = channelID
        self.info = info if info else {}
        
    def __str__(self):
        return f"Alert(type={self.type}, serverID={self.serverID}, channelID={self.channelID}, info={self.info})"

    def __repr__(self):
        return self.__str__()
        
class AlertType(Enum):
    PROBLEM = "problem"
    CONTEST_TIME_AWAY = "contest-time-away"
    DAILY_PROBLEM = "daily-problem"
    WEEKLY_CONTEST = "weekly-contest"
    BIWEEKLY_CONTEST = "biweekly-contest"