import discord
from discord import app_commands

from models.server import Server
from models.app import App
from buckets.static_time_bucket import StaticTimeAlert
from errors.simple_exception import SimpleException
from view.error_embed import ErrorEmbed
from view.positive_embed import PositiveEmbed


class ServerConfigView(discord.ui.View):
    def __init__(self, server: Server, app: App, setting: str):
        super().__init__(timeout=60)
        try:
            match setting:
                case "upcomingcontests":
                    self.add_item(ContestTimeAlertMenu(server, app))
                    self.add_item(ContestTimeIntervalsMenu(server, app))
                case "staticalerts":
                    self.add_item(WeeklyContestAlertMenu(server, app))
                    self.add_item(BiweeklyContestAlertMenu(server, app))
                    self.add_item(DailyProblemAlertMenu(server, app))
                case "other":
                    self.add_item(TimezoneSelector(server))
                    self.add_item(AllowDuplicatesMenu(server, app))
                    self.add_item(UseAlertRoleMenu(server, app))       
                    self.add_item(RoleSelector(server))   
                    self.add_item(ChannelSelector(server))
                case "timezone":
                    self.add_item(TimezoneSelector(server))
                case _:
                    raise SimpleException("SERVERCONFVIEW", "Backend failure")
        except Exception as e:
            raise SimpleException("SERVERCONFVIEW", "Failed to load server config view", "There was an error loading the server config view. Please try again later.") from e    

# FIXME: These 3 static alert menu classes can def be combined to reduce some copy pasted code
# =================================
# WEEKLY CONTEST ALERT MENU
# =================================
class WeeklyContestAlertMenu(discord.ui.Select):
    def __init__(self, server: Server, app: App):
        self.server = server
        self.app = app

        options = [
            discord.SelectOption(label="ON", description="Enable weekly contest alerts", value=True),
            discord.SelectOption(label="OFF", description="Disable weekly contest alerts", value=False),
        ]

        super().__init__(
            placeholder=f"Weekly Contest Alerts \t({'ON' if server.settings.weeklyContestAlerts else 'OFF'})",
            options=options, min_values=1, max_values=1,
        )

    async def callback(self, interaction: discord.Interaction):
        if len(self.values) != 1:
            embed = ErrorEmbed("CONTSQSEMB", "Invalid Selection", "Please select either ON or OFF to change the weekly contest alert setting.")
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        change = self.values[0] == "True"  # convert to bool
        result = self.app.synchronizer.changeStaticAlert(
            self.server.serverID, StaticTimeAlert.WEEKLY_CONTEST, change)
        if not result:
            embed = ErrorEmbed("CONTSQSEMB", "Failed to Change Weekly Contest Alerts", "There was an error changing the weekly contest alert setting.")
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        word = "enabled" if change else "disabled"
        await interaction.response.send_message(embed=PositiveEmbed("Weekly Contest Alerts Updated", f"Weekly contest alerts are now **{word}**"), ephemeral=True)

# =================================
# BIWEEKLY CONTEST ALERT MENU
# =================================
class BiweeklyContestAlertMenu(discord.ui.Select):
    def __init__(self, server: Server, app: App):
        self.server = server
        self.app = app

        options = [
            discord.SelectOption(label="ON", description="Enable biweekly contest alerts", value=True),
            discord.SelectOption(label="OFF", description="Disable biweekly contest alerts", value=False),
        ]

        super().__init__(
            placeholder=f"Biweekly Contest Alerts \t({'ON' if server.settings.biweeklyContestAlerts else 'OFF'})",
            options=options, min_values=1, max_values=1,
        )

    async def callback(self, interaction: discord.Interaction):
        if len(self.values) != 1:
            embed = ErrorEmbed("CONTSQSEMB", "Invalid Selection", "Please select either ON or OFF to change the biweekly contest alert setting.")
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        change = self.values[0] == "True"  # convert to bool
        result = self.app.synchronizer.changeStaticAlert(
            self.server.serverID, StaticTimeAlert.BIWEEKLY_CONTEST, change)
        if not result:
            embed = ErrorEmbed("CONTSQSEMB", "Failed to Change Biweekly Contest Alerts", "There was an error changing the biweekly contest alert setting.")
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        word = "enabled" if change else "disabled"
        await interaction.response.send_message(embed=PositiveEmbed("Biweekly Contest Alerts Updated", f"Biweekly contest alerts are now **{word}**"), ephemeral=True)

# =================================
# DAILY PROBLEM ALERT MENU
# =================================
class DailyProblemAlertMenu(discord.ui.Select):
    def __init__(self, server: Server, app: App):
        self.server = server
        self.app = app

        options = [
            discord.SelectOption(label="ON", description="Enable daily problem alerts", value=True),
            discord.SelectOption(label="OFF", description="Disable daily problem alerts", value=False),
        ]

        super().__init__(
            placeholder=f"Daily Problem Alerts \t({'ON' if server.settings.officialDailyAlerts else 'OFF'})",
            options=options, min_values=1, max_values=1,
        )

    async def callback(self, interaction: discord.Interaction):
        if len(self.values) != 1:
            embed = ErrorEmbed("CONTSQSEMB", "Invalid Selection", "Please select either ON or OFF to change the daily problem alert setting.")
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        change = self.values[0] == "True"  # convert to bool
        result = self.app.synchronizer.changeStaticAlert(
            self.server.serverID, StaticTimeAlert.DAILY_PROBLEM, change)
        if not result:
            embed = ErrorEmbed("DAILYPROB", "Failed to Change Daily Problem Alerts", "There was an error changing the daily problem alert setting.")
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        word = "enabled" if change else "disabled"
        await interaction.response.send_message(embed=PositiveEmbed("Daily Problem Alerts Updated", f"Daily problem alerts are now **{word}**"), ephemeral=True)

# =================================
# CONTEST TIME INTERVALS
# =================================
# change the min/max values
class ContestTimeIntervalsMenu(discord.ui.Select):
    def __init__(self, server: Server, app: App):
        self.server = server
        self.app = app
        
        options = [
            discord.SelectOption(label="15 mins", description="Give an alert 15 minutes before the contest starts", value="15:15 mins"),
            discord.SelectOption(label="30 mins", description="Give an alert 30 minutes before the contest starts", value="30:30 mins"),
            discord.SelectOption(label="1 hr", description="Give an alert 1 hour before the contest starts", value="60:1 hr"),
            discord.SelectOption(label="2 hrs", description="Give an alert 2 hours before the contest starts", value="120:2 hrs"),
            discord.SelectOption(label="6 hrs", description="Give an alert 6 hours before the contest starts", value="360:6 hrs"),
            discord.SelectOption(label="12 hrs", description="Give an alert 12 hours before the contest starts", value="720:12 hrs"),
            discord.SelectOption(label="1 day", description="Give an alert 1 day before the contest starts", value="1440:1 day"),
        ]

        timeTable = {15: "15 mins", 30: "30 mins", 60: "1 hr", 120: "2 hrs", 360: "6 hrs", 720: "12 hrs", 1440: "1 day"}
        intervals = server.settings.contestTimeIntervals if server.settings.contestTimeIntervals is not None else []
        sorted_intervals = sorted(intervals)
        super().__init__(
            placeholder=f"Contest Time Intervals \t({', '.join([timeTable.get(i, str(i)) for i in sorted_intervals])})",
            options=options, min_values=1, max_values=len(options),
        )

    async def callback(self, interaction: discord.Interaction):
        if len(self.values) <= 0:
            embed = ErrorEmbed("CONTSQS", "No Intervals Selected", "You must select at least one interval to change the contest time alerts.")
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        if not self.server.settings.contestTimeAlerts:
            embed = ErrorEmbed("CONTSQS", "Contest Time Alerts Disabled", "You must enable **Contest Time Alerts** to change the intervals.")
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        newIntervals = [int(value.split(":")[0]) for value in self.values]
        displayIntervals = [value.split(":")[1] for value in self.values]
        result = self.app.synchronizer.changeAlertIntervals(self.server.serverID, newIntervals)
        if not result:
            embed = ErrorEmbed("CONTSQS", "Failed to Change Intervals", "There was an error changing the contest time alert intervals.")
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        await interaction.response.send_message(embed=PositiveEmbed("Contest Intervals Updated", f"Contest Intervals have been updated to {', '.join(displayIntervals)}"), ephemeral=True)
        self.app.contestTimeBucket.printBucketClean()

# =================================
# CONTEST TIME ALERTS
# =================================
class ContestTimeAlertMenu(discord.ui.Select):
    def __init__(self, server: Server, app: App):
        self.server = server
        self.app = app

        options = [
            discord.SelectOption(label="ON", description="Enable upcoming contest alerts using your intervals", value=True),
            discord.SelectOption(label="OFF", description="Disable upcoming contest alerts using your intervals", value=False),
        ]

        super().__init__(
            placeholder=f"Upcoming Contest Alerts \t({'ON' if server.settings.contestTimeAlerts else 'OFF'})",
            options=options, min_values=1, max_values=1,
        )

    async def callback(self, interaction: discord.Interaction):
        if len(self.values) != 1:
            embed = ErrorEmbed("CONTSQS", "Invalid Selection", "Please select either ON or OFF to change the upcoming contest alert setting.")
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        change = self.values[0] == "True"  # convert to bool
        result = self.app.synchronizer.changeContestAlertParticpation(self.server.serverID, change)
        if not result:
            embed = ErrorEmbed("CONTSQS", "Failed to Change Upcoming Contest Alerts", "There was an error changing the upcoming contest alert setting.")
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return 

        word = "enabled" if change else "disabled"
        await interaction.response.send_message(embed=PositiveEmbed("Upcoming Contest Alerts Updated", f"**Upcoming contest alerts** are now {word} on your selected intervals"), ephemeral=True)

# =================================
# DUPLICATES ALLOWED
# =================================
class AllowDuplicatesMenu(discord.ui.Select):
    def __init__(self, server: Server, app: App):
        self.server = server
        self.app = app

        options = [
            discord.SelectOption(label="ON", description="Allow duplicate problems", value=True),
            discord.SelectOption(label="OFF", description="Don't allow duplicate problems", value=False),
        ]

        super().__init__(
            placeholder=f"Allow Duplicates \t({'ON' if server.settings.duplicatesAllowed else 'OFF'})",
            options=options, min_values=1, max_values=1,
        )

    async def callback(self, interaction: discord.Interaction):
        if len(self.values) != 1:
            embed = ErrorEmbed("DUPSELECT", "Invalid Selection", "Please select either ON or OFF to change the duplicates setting.")
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        change = self.values[0] == "True"  # convert to bool
        self.server.settings.duplicatesAllowed = change
        self.server.toJSON()  # save the change

        word = "enabled" if change else "disabled"
        await interaction.response.send_message(embed=PositiveEmbed("Duplicates Updated", f"**Duplicates** are now {word}"), ephemeral=True)

# =================================
# USE ALERT ROLE?
# =================================
class UseAlertRoleMenu(discord.ui.Select):
    def __init__(self, server: Server, app: App):
        self.server = server
        self.app = app

        options = [
            discord.SelectOption(label="ON", description="Use alert role for notifications", value=True),
            discord.SelectOption(label="OFF", description="Don't use alert role for notifications", value=False),
        ]

        super().__init__(
            placeholder=f"Use Alert Role \t({'ON' if server.settings.useAlertRole else 'OFF'})",
            options=options, min_values=1, max_values=1,
        )

    async def callback(self, interaction: discord.Interaction):
        if len(self.values) != 1:
            embed  = ErrorEmbed("ALERTROLE", "Invalid Selection", "Please select either ON or OFF to change the alert role setting.")
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        change = self.values[0] == "True"  # convert to bool
        self.server.settings.useAlertRole = change
        self.server.toJSON()  # save the change

        word = "enabled" if change else "disabled"
        await interaction.response.send_message(embed=PositiveEmbed("Alert Role Updated", f"**Alert Role** is now {word}"), ephemeral=True)

# =================================
# ROLE SELECTOR 
# =================================
class RoleSelector(discord.ui.RoleSelect):
    def __init__(self, server: Server):
        super().__init__(
            placeholder="Select Alert Role - Type Role Name Here",
        )
        self.server = server
        self.min_values = 1
        self.max_values = 1

    async def callback(self, interaction: discord.Interaction):
        if self.values is None or len(self.values) == 0:
            embed = ErrorEmbed("ROLES", "No role selected", "Please select a valid role from the dropdown menu.")
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        
        # update the server settings with the selected role
        role = self.values[0]
        self.server.settings.alertRoleID = int(role.id)
        self.server.toJSON()
        await interaction.response.send_message(embed=PositiveEmbed("Server Role Updated", f"Server Role set to: <@&{role.id}>"), ephemeral=True)

class ChannelSelector(discord.ui.ChannelSelect):
    def __init__(self, server: Server):
        super().__init__(
            placeholder="Select Output Channel - Type Channel Name Here",
            channel_types=[discord.ChannelType.text],  # only allow text channels
        )
        self.server = server
        self.min_values = 1
        self.max_values = 1

    async def callback(self, interaction: discord.Interaction):
        if self.values is None or len(self.values) == 0:
            embed = ErrorEmbed("CHNSELVW", "No channel selected", "Please select a valid text channel from the dropdown menu.")
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        channel = self.values[0]
        if channel.type != discord.ChannelType.text:
            code = "CHNSELVW"
            msg = "The selected channel is not a text channel."
            help = "If your channel is not listed, try doing `/setchannel #channel_name` to set it as the output channel directly."
            embed = ErrorEmbed(code, msg, help)
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
            
        # update the server settings with the selected channel
        channel = self.values[0]
        self.server.settings.postingChannelID = int(channel.id)
        self.server.toJSON()
        await interaction.response.send_message(embed=PositiveEmbed("Server Channel Updated", f"Server Channel set to: <#{channel.id}>"), ephemeral=True)
        
class TimezoneSelector(discord.ui.Select):
    def __init__(self, server: Server):
        timezone_map = [
            ("UTC", "UTC"),
            ("EST", "America/New_York (Eastern Time)"),
            ("CST", "America/Chicago (Central Time, US)"),
            ("MST", "America/Denver (Mountain Time)"),
            ("PST", "America/Los_Angeles (Pacific Time)"),
            ("GMT", "Europe/London (London)"),
            ("CET", "Europe/Berlin/Paris (Central European Time)"),
            ("MSK", "Europe/Moscow (Moscow)"),
            ("IST", "Asia/Kolkata (India Standard Time)"),
            ("CST-CHINA", "Asia/Shanghai (China Standard Time)"),
            ("JST", "Asia/Tokyo (Japan Standard Time)"),
            ("SGT", "Asia/Singapore (Singapore Time)"),
            ("AEST", "Australia/Sydney (Australian Eastern Standard Time)"),
            ("NZST", "Pacific/Auckland (New Zealand Standard Time)"),
        ]
        options = [discord.SelectOption(label=f"{zone}", description=descriptor, value=zone) for zone, descriptor in timezone_map]

        super().__init__(
            placeholder=f"Select Timezone ({server.settings.timezone})",
            options=options, min_values=1, max_values=1,
        )
        self.server = server

    async def callback(self, interaction: discord.Interaction):
        if len(self.values) != 1:
            embed = ErrorEmbed("TIMEZONE", "Invalid selection", "Please select a valid timezone from the dropdown menu.")
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        
        self.server.settings.timezone = self.values[0]
        self.server.toJSON()
        embed = PositiveEmbed("Timezone Updated", f"Timezone set to: {self.values[0]}")
        if interaction.response.is_done():
            await interaction.followup.send(embed=embed, ephemeral=True)
        else:
            await interaction.response.send_message(embed=embed, ephemeral=True)
        
        