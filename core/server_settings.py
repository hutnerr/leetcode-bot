class ServerSettings:

    def __init__(self, postingChannelID: int = None,
                 weeklyContestAlerts: bool = False,
                 biweeklyContestAlerts: bool = False,
                 officialDailyAlerts: bool = False):

        self.postingChannelID = postingChannelID
        self.weeklyContestAlerts = weeklyContestAlerts
        self.biweeklyContestAlerts = biweeklyContestAlerts
        self.officialDailyAlerts = officialDailyAlerts

    def toJSON(self) -> dict:
        return {
            "postingChannelID": self.postingChannelID,
            "weeklyContestAlerts": self.weeklyContestAlerts,
            "biweeklyContestAlerts": self.biweeklyContestAlerts,
            "officialDailyAlerts": self.officialDailyAlerts,
        }

    def __str__(self) -> str:
        return (f"postingChannelID={self.postingChannelID}\n"
                f"\t\tweeklyContestAlerts={self.weeklyContestAlerts}\n"
                f"\t\tbiweeklyContestAlerts={self.biweeklyContestAlerts}\n"
                f"\t\tofficialDailyAlerts={self.officialDailyAlerts}\n"
               )

    @staticmethod
    def buildFromJSON(settings: dict) -> "ServerSettings":
        return ServerSettings(
            postingChannelID=settings.get("postingChannelID"),
            weeklyContestAlerts=settings.get("weeklyContestAlerts", False),
            biweeklyContestAlerts=settings.get("biweeklyContestAlerts", False),
            officialDailyAlerts=settings.get("officialDailyAlerts", False)
        )
