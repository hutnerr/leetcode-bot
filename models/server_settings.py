# composition piece used by a Server
# just contains additional server settings 
class ServerSettings:
    def __init__(self,
                 postingChannelID: int = None,            # the channel ID where alerts get posted
                 weeklyContestAlerts: bool = False,       # whether to alert for weekly contests
                 biweeklyContestAlerts: bool = False,     # whether to alert for biweekly contests
                 officialDailyAlerts: bool = False,       # whether to alert for official daily problems
                 contestTimeIntervals: list[int] = None,  # list of intervals in minutes for contest time alerts
                 contestTimeAlerts: bool = False,         # whether to alert for contest time
                 duplicatesAllowed: bool = False,         # whether duplicates are allowed in the problem selection
                 alertRoleID: int = None,                 # the role ID to mention in alerts, if applicable
                 useAlertRole: bool = False               # whether to use the alert role in the alerts
                 ):
        self.postingChannelID = postingChannelID
        self.weeklyContestAlerts = weeklyContestAlerts
        self.biweeklyContestAlerts = biweeklyContestAlerts
        self.officialDailyAlerts = officialDailyAlerts
        self.contestTimeIntervals = contestTimeIntervals if contestTimeIntervals is not None else []
        self.contestTimeAlerts = contestTimeAlerts
        self.duplicatesAllowed = duplicatesAllowed
        self.alertRoleID = alertRoleID
        self.useAlertRole = useAlertRole

    def __str__(self) -> str:
        return (f"postingChannelID={self.postingChannelID}\n"
                f"\t\tweeklyContestAlerts={self.weeklyContestAlerts}\n"
                f"\t\tbiweeklyContestAlerts={self.biweeklyContestAlerts}\n"
                f"\t\tofficialDailyAlerts={self.officialDailyAlerts}\n"
                f"\t\tcontestTimeIntervals={self.contestTimeIntervals}\n"
                f"\t\tcontestTimeAlerts={self.contestTimeAlerts}\n"
                f"\t\tduplicatesAllowed={self.duplicatesAllowed}\n"
                f"\t\talertRoleID={self.alertRoleID}\n"
                f"\t\tuseAlertRole={self.useAlertRole}\n"
                )

    def toJSON(self) -> dict:
        return {
            "postingChannelID": self.postingChannelID,
            "weeklyContestAlerts": self.weeklyContestAlerts,
            "biweeklyContestAlerts": self.biweeklyContestAlerts,
            "officialDailyAlerts": self.officialDailyAlerts,
            "contestTimeIntervals": self.contestTimeIntervals,
            "contestTimeAlerts": self.contestTimeAlerts,
            "duplicatesAllowed": self.duplicatesAllowed,
            "alertRoleID": self.alertRoleID,
            "useAlertRole": self.useAlertRole
        }

    @staticmethod
    def buildFromJSON(settings: dict) -> "ServerSettings":
        return ServerSettings(
            postingChannelID=settings.get("postingChannelID"),
            weeklyContestAlerts=settings.get("weeklyContestAlerts", False),
            biweeklyContestAlerts=settings.get("biweeklyContestAlerts", False),
            officialDailyAlerts=settings.get("officialDailyAlerts", False),
            contestTimeIntervals=settings.get("contestTimeIntervals", []),
            contestTimeAlerts=settings.get("contestTimeAlerts", []),
            duplicatesAllowed=settings.get("duplicatesAllowed", False),
            alertRoleID=settings.get("alertRoleID"),
            useAlertRole=settings.get("useAlertRole", False)
        )
