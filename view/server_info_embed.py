import discord.embeds
from models.server import Server

from view.server_config_view import ServerConfigView

class ServerInfoEmbed(discord.Embed):
    def __init__(self, server: Server, guild: discord.Guild):
        super().__init__(title=f"{guild.name} Config")
        self.color = discord.Color.blurple()
        # self.set_thumbnail(url=guild.icon)
        # self.set_image(url=guild.icon.url)
        self.timeTable = {15: "15 mins", 30: "30 mins", 60: "1 hr", 120: "2 hrs", 360: "6 hrs", 720: "12 hrs", 1440: "1 day"}
        self.set_footer(text="Channge the config using /sconfig. Delete with /delserver.")
        
        upcomingContestsString = ""
        upcomingContestsString += f"Contest Alerts.\n> `{ 'Enabled' if server.settings.contestTimeAlerts else 'Disabled'}`\n"
        upcomingContestsString += "Intervals.\n"
        for interval in server.settings.contestTimeIntervals:
            upcomingContestsString += f"> `{self.timeTable[interval]}`\n"
        self.add_field(name="Upcoming Contest Config", value=upcomingContestsString, inline=True)
        
        staticTimeAlerts = ""
        staticTimeAlerts += f"Weekly Contest Alerts.\n> `{ 'Enabled' if server.settings.weeklyContestAlerts else 'Disabled'}`\n"
        staticTimeAlerts += f"Biweekly Contest Alerts.\n> `{ 'Enabled' if server.settings.biweeklyContestAlerts else 'Disabled'}`\n"
        staticTimeAlerts += f"Official Daily Alerts.\n> `{ 'Enabled' if server.settings.officialDailyAlerts else 'Disabled'}`\n"
        self.add_field(name="\nStatic Times Config", value=staticTimeAlerts, inline=True)
        
        otherConfigs = ""
        otherConfigs += f"Timezone.\n> `{server.settings.timezone}`\n"
        otherConfigs += f"Duplicates Allowed.\n> `{ 'Enabled' if server.settings.duplicatesAllowed else 'Disabled'}`\n"
        otherConfigs += f"Use Alert Role.\n> `{ 'Enabled' if server.settings.useAlertRole else 'Disabled'}`\n"
        otherConfigs += f"Alert Role.\n> {f'<@&{server.settings.alertRoleID}>' if server.settings.alertRoleID else 'None'}\n"
        otherConfigs += f"Bot Channel.\n> <#{server.settings.postingChannelID}>\n"
        self.add_field(name="\nOther Configs", value=otherConfigs, inline=True)
