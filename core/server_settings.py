class ServerSettings:

    # long line lol sorry
    def __init__(self, postingChannelID: int = None, weeklyContestAlerts: bool = False, biweeklyContestAlerts: bool = False, officialDailyAlerts: bool = False, contestAlertIntervals: list[int] = None, duplicatesAllowed: bool = False):
        self.postingChannelID = postingChannelID
        self.weeklyContestAlerts = weeklyContestAlerts
        self.biweeklyContestAlerts = biweeklyContestAlerts
        self.officialDailyAlerts = officialDailyAlerts
        self.contestAlertIntervals = contestAlertIntervals if contestAlertIntervals is not None else []
        self.duplicatesAllowed = duplicatesAllowed

    def toJSON(self) -> dict:
        return {
            "postingChannelID": self.postingChannelID,
            "weeklyContestAlerts": self.weeklyContestAlerts,
            "biweeklyContestAlerts": self.biweeklyContestAlerts,
            "officialDailyAlerts": self.officialDailyAlerts,
            "contestAlertIntervals": self.contestAlertIntervals,
            "duplicatesAllowed": self.duplicatesAllowed
        }

    def __str__(self) -> str:
        return (f"postingChannelID={self.postingChannelID}\n"
                f"\t\tweeklyContestAlerts={self.weeklyContestAlerts}\n"
                f"\t\tbiweeklyContestAlerts={self.biweeklyContestAlerts}\n"
                f"\t\tofficialDailyAlerts={self.officialDailyAlerts}\n"
                f"\t\tcontestAlertIntervals={self.contestAlertIntervals}\n"
                f"\t\tduplicatesAllowed={self.duplicatesAllowed}\n"
                )

    @staticmethod
    def buildFromJSON(settings: dict) -> "ServerSettings":
        return ServerSettings(
            postingChannelID=settings.get("postingChannelID"),
            weeklyContestAlerts=settings.get("weeklyContestAlerts", False),
            biweeklyContestAlerts=settings.get("biweeklyContestAlerts", False),
            officialDailyAlerts=settings.get("officialDailyAlerts", False),
            contestAlertIntervals=settings.get("contestAlertIntervals", []),
            duplicatesAllowed=settings.get("duplicatesAllowed", False)
        )
