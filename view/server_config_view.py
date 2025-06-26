import discord
from models.server import Server
from models.app import App
from buckets.static_time_bucket import StaticTimeAlert
from errors.simple_exception import SimpleException

class ServerConfigView(discord.ui.View):
    def __init__(self, server: Server, app: App, setting: str):
        super().__init__(timeout=60)
        match setting:
            case "upcomingcontests":
                self.add_item(ContestTimeAlertMenu(server, app))
                self.add_item(ContestTimeIntervalsMenu(server, app))
            case "staticalerts":
                self.add_item(WeeklyContestAlertMenu(server, app))
                self.add_item(BiweeklyContestAlertMenu(server, app))
                self.add_item(DailyProblemAlertMenu(server, app))
            case "other":
                self.add_item(AllowDuplicatesMenu(server, app))
                self.add_item(UseAlertRoleMenu(server, app))          
            case _:
                raise SimpleException("INVALID SETTING")

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
            await interaction.response.send_message("Invalid selection", ephemeral=True)
            return

        change = self.values[0] == "True"  # convert to bool
        result = self.app.synchronizer.changeStaticAlert(
            self.server.serverID, StaticTimeAlert.WEEKLY_CONTEST, change)
        if not result:
            raise SimpleException("FAILED CHANGING")

        word = "enabled" if change else "disabled"
        await interaction.response.send_message(f"**Weekly contest alerts** are now {word}", ephemeral=True)

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
            await interaction.response.send_message("Invalid selection", ephemeral=True)
            return

        change = self.values[0] == "True"  # convert to bool
        result = self.app.synchronizer.changeStaticAlert(
            self.server.serverID, StaticTimeAlert.BIWEEKLY_CONTEST, change)
        if not result:
            raise SimpleException("FAILED CHANGING")

        word = "enabled" if change else "disabled"
        await interaction.response.send_message(f"**Biweekly contest alerts** are now {word}", ephemeral=True)

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
            await interaction.response.send_message("Invalid selection", ephemeral=True)
            return

        change = self.values[0] == "True"  # convert to bool
        result = self.app.synchronizer.changeStaticAlert(
            self.server.serverID, StaticTimeAlert.DAILY_PROBLEM, change)
        if not result:
            raise SimpleException("FAILED CHANGING")

        word = "enabled" if change else "disabled"
        await interaction.response.send_message(f"**Daily problem alerts** are now {word}", ephemeral=True)

# =================================
# CONTEST TIME INTERVALS
# =================================
# change the min/max values
class ContestTimeIntervalsMenu(discord.ui.Select):
    def __init__(self, server: Server, app: App):
        self.server = server
        self.app = app
        
        options = [
            discord.SelectOption(label="15 mins", description="Give 15 minutes before the contest starts", value=15),
            discord.SelectOption(label="30 mins", description="Give 30 minutes before the contest starts", value=30),
            discord.SelectOption(label="1 hr", description="Give 1 hour before the contest starts", value=60),
            discord.SelectOption(label="2 hrs", description="Give 2 hours before the contest starts", value=120),
            discord.SelectOption(label="6 hrs", description="Give 6 hours before the contest starts", value=360),
            discord.SelectOption(label="12 hrs", description="Give 12 hours before the contest starts", value=720),
            discord.SelectOption(label="1 day", description="Give 1 day before the contest starts", value=1440),
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
            await interaction.response.send_message("Invalid selection", ephemeral=True)
            return
        
        if not self.server.settings.contestTimeAlerts:
            await interaction.response.send_message("**Contest Time Alerts** must be enabled to change intervals", ephemeral=True)
            return
    
        newIntervals = [int(interval) for interval in self.values]
        result = self.app.synchronizer.changeAlertIntervals(self.server.serverID, newIntervals)
        if not result:
            raise SimpleException("FAILED CHANGING")

        await interaction.response.send_message("**Contest Intervals** have been updated", ephemeral=True)
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
            await interaction.response.send_message("Invalid selection", ephemeral=True)
            return

        change = self.values[0] == "True"  # convert to bool
        result = self.app.synchronizer.changeContestAlertParticpation(self.server.serverID, change)
        if not result:
            raise SimpleException("FAILED CHANGING")

        word = "enabled" if change else "disabled"
        await interaction.response.send_message(f"**Upcoming contest alerts** are now {word} on your selected intervals", ephemeral=True)

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
            await interaction.response.send_message("Invalid selection", ephemeral=True)
            return

        change = self.values[0] == "True"  # convert to bool
        self.server.settings.duplicatesAllowed = change
        self.server.toJSON()  # save the change

        word = "enabled" if change else "disabled"
        await interaction.response.send_message(f"**Duplicates** are now {word}", ephemeral=True)
        
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
            await interaction.response.send_message("Invalid selection", ephemeral=True)
            return

        change = self.values[0] == "True"  # convert to bool
        self.server.settings.useAlertRole = change
        self.server.toJSON()  # save the change

        word = "enabled" if change else "disabled"
        await interaction.response.send_message(f"**Alert Role** is now {word}", ephemeral=True)
