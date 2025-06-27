import discord.embeds
from models.alert import Alert, AlertType

class AlertEmbed(discord.Embed):
    def __init__(self, alert: Alert):
        super().__init__(url=alert.info.get("url", None))
        
        bellIconURL = "https://images.icon-icons.com/3653/PNG/512/bell_notification_icon_228288.png"
        leetCodeIconURL = "https://leetcode.com/static/images/LeetCode_logo_rvs.png"
        clockIconURL = "https://assets.streamlinehq.com/image/private/w_512,h_512,ar_1/f_auto/v1/icons/1/alarm-clock-8x1uhzi8lnqnxzawr60ih.png/alarm-clock-jck7ltg29a4dg77hlu0ks.png?_a=DATAdtAAZAA0"

        self.description = alert.info.get("alertString")
        match alert.type:
            case AlertType.WEEKLY_CONTEST:
                self.title = "Weekly Contest Alert"
                self.set_thumbnail(url=bellIconURL)
                self.color = discord.Color.blue()
            case AlertType.BIWEEKLY_CONTEST:
                self.title = "Biweekly Contest Alert"
                self.set_thumbnail(url=bellIconURL)
                self.color = discord.Color.blue()
            case AlertType.DAILY_PROBLEM:
                self.title = "Daily Problem Alert"
                self.set_thumbnail(url=leetCodeIconURL)
                self.color = discord.Color.orange()
            case AlertType.CONTEST_TIME_AWAY:
                self.title = "Upcoming Contest Alert"
                self.set_thumbnail(url=clockIconURL)
                self.color = discord.Color.blue()
            case _:
                self.description = "An alert has been triggered!"

