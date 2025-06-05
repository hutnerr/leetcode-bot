class ServerSettings:

    # long line lol sorry
    def __init__(self, postingChannelID: int = None, weeklyContestAlerts: bool = False, biweeklyContestAlerts: bool = False, officialDailyAlerts: bool = False, contestAlertIntervals: list[int] = None, duplicatesAllowed: bool = False, alertRoleID: int = None, useAlertRole: bool = False):
        self.postingChannelID = postingChannelID
        self.weeklyContestAlerts = weeklyContestAlerts
        self.biweeklyContestAlerts = biweeklyContestAlerts
        self.officialDailyAlerts = officialDailyAlerts
        self.contestAlertIntervals = contestAlertIntervals if contestAlertIntervals is not None else []
        self.duplicatesAllowed = duplicatesAllowed
        self.alertRoleID = alertRoleID
        self.useAlertRole = useAlertRole

    def toJSON(self) -> dict:
        return {
            "postingChannelID": self.postingChannelID,
            "weeklyContestAlerts": self.weeklyContestAlerts,
            "biweeklyContestAlerts": self.biweeklyContestAlerts,
            "officialDailyAlerts": self.officialDailyAlerts,
            "contestAlertIntervals": self.contestAlertIntervals,
            "duplicatesAllowed": self.duplicatesAllowed,
            "alertRoleID": self.alertRoleID,
            "useAlertRole": self.useAlertRole
        }

    def __str__(self) -> str:
        return (f"postingChannelID={self.postingChannelID}\n"
                f"\t\tweeklyContestAlerts={self.weeklyContestAlerts}\n"
                f"\t\tbiweeklyContestAlerts={self.biweeklyContestAlerts}\n"
                f"\t\tofficialDailyAlerts={self.officialDailyAlerts}\n"
                f"\t\tcontestAlertIntervals={self.contestAlertIntervals}\n"
                f"\t\tduplicatesAllowed={self.duplicatesAllowed}\n"
                f"\t\talertRoleID={self.alertRoleID}\n"
                f"\t\tuseAlertRole={self.useAlertRole}\n"
                )

    @staticmethod
    def buildFromJSON(settings: dict) -> "ServerSettings":
        return ServerSettings(
            postingChannelID=settings.get("postingChannelID"),
            weeklyContestAlerts=settings.get("weeklyContestAlerts", False),
            biweeklyContestAlerts=settings.get("biweeklyContestAlerts", False),
            officialDailyAlerts=settings.get("officialDailyAlerts", False),
            contestAlertIntervals=settings.get("contestAlertIntervals", []),
            duplicatesAllowed=settings.get("duplicatesAllowed", False),
            alertRoleID=settings.get("alertRoleID"),
            useAlertRole=settings.get("useAlertRole", False)
        )
