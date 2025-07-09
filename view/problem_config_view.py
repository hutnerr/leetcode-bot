import discord


from models.server import Server
from models.app import App
from models.problem import Problem

from utils import datetime_helper as timeh

from errors.simple_exception import SimpleException

from view.positive_embed import PositiveEmbed

dayTable = {
            0: "Sunday",
            1: "Monday",
            2: "Tuesday",
            3: "Wednesday",
            4: "Thursday",
            5: "Friday",
            6: "Saturday"
}

# gens a string thats like
# Problems will be sent at 12:00 AM for every day of the week.
# Problems will be sent at 1:15 PM on Monday and Wednesday. 
def getProblemSentString(problem: Problem, totz: str) -> str:
    hour, minute = timeh.convertFromLocalTimeZone(problem.hour, problem.interval * 15, totz)

    hour12 = hour % 12
    hour12 = 12 if hour12 == 0 else hour12
    ampm = "AM" if hour < 12 else "PM"
    minute = minute * 15

    days = [dayTable[day] for day in problem.dows] if problem.dows else []
    if len(days) == 7:
        daysStr = "for every day of the week"
    elif len(days) == 1:
        daysStr = f"on {days[0]}"
    elif len(days) == 2:
        daysStr = f"on {days[0]} and {days[1]}"
    elif len(days) > 2:
        daysStr = f"on {', '.join(days[:-1])}, and {days[-1]}"
    else:
        daysStr = "on no days"

    return f"Problems will be sent at **{hour12}:{minute:02}** {ampm} {daysStr}."

class ProblemConfigView(discord.ui.View):
    def __init__(self, server: Server, problem: Problem, app: App):
        super().__init__(timeout=60)    
        self.add_item(DifficultiesSelect(server, problem, app))
        self.add_item(PremiumSelect(server, problem, app))
        self.add_item(DaysOfWeekSelect(server, problem, app))
        self.add_item(HourSelect(server, problem, app))
        self.add_item(IntervalSelect(server, problem, app))
        
class DifficultiesSelect(discord.ui.Select):
    def __init__(self, server: Server, problem: Problem, app: App):
        self.server = server
        self.problem = problem
        self.app = app

        options = [
            discord.SelectOption(label="Easy", description="Easy problems may be selected", value="easy"),
            discord.SelectOption(label="Medium", description="Medium problems may be selected", value="medium"),
            discord.SelectOption(label="Hard", description="Hard problems may be selected", value="hard"),
        ]

        super().__init__(
            placeholder=f"Select Problem Difficulty ({', '.join([d.capitalize() for d in problem.difficulties]) if problem.difficulties else 'None'})",
            options=options, min_values=1, max_values=3,
        )

    async def callback(self, interaction: discord.Interaction):
        if len(self.values) <= 0:
            await interaction.response.send_message("Invalid selection", ephemeral=True)
            return

        selectedDifficulties = self.values
        self.problem.difficulties = selectedDifficulties
        difString = f"Problem difficulty is now set to {', '.join(selectedDifficulties)}"
        embed = PositiveEmbed("Problem Difficulty Set", difString)
        if interaction.response.is_done():
            await interaction.followup.send(embed=embed, ephemeral=True)
        else:
            await interaction.response.send_message(embed=embed, ephemeral=True)
        self.app.synchronizer.addProblem(self.problem)
        self.server.toJSON()

class DaysOfWeekSelect(discord.ui.Select):
    def __init__(self, server: Server, problem: Problem, app: App):
        self.server = server
        self.problem = problem
        self.app = app

        options = [
            discord.SelectOption(label="Sunday", description="Problems will be sent on Sunday at set time", value=0),
            discord.SelectOption(label="Monday", description="Problems will be sent on Monday at set time", value=1),
            discord.SelectOption(label="Tuesday", description="Problems will be sent on Tuesday at set time", value=2),
            discord.SelectOption(label="Wednesday", description="Problems will be sent on Wednesday at set time", value=3),
            discord.SelectOption(label="Thursday", description="Problems will be sent on Thursday at set time", value=4),
            discord.SelectOption(label="Friday", description="Problems will be sent on Friday at set time", value=5),
            discord.SelectOption(label="Saturday", description="Problems will be sent on Saturday at set time", value=6),
        ]

        # Convert problem.dows (list of ints) to day names for placeholder
        selectedDays = [dayTable.get(day, "Unknown") for day in problem.dows] if problem.dows else []
        super().__init__(
            placeholder=f"Select Problem Days ({', '.join(selectedDays) if selectedDays else 'None'})",
            options=options, min_values=1, max_values=7,
        )

    async def callback(self, interaction: discord.Interaction):
        if len(self.values) <= 0:
            await interaction.response.send_message("Invalid selection", ephemeral=True)
            return
                
        remove = self.app.synchronizer.removeProblem(self.problem)
        if not remove:
            raise SimpleException("REMOFAIL", "Failed to remove the old problem before setting the new one. This should not happen, please report this issue using `/report`. Also please `/delproblem` and re-add the problem. Sorry for the inconvenience.")

        selectedDays = self.values
        self.problem.dows = [int(day) for day in selectedDays]

        add = self.app.synchronizer.addProblem(self.problem)
        if not add:
            raise SimpleException("ADDPFAIL", "Failed to add the new problem after setting the days. This should not happen, please report this issue using `/report`. Also please `/delproblem` and re-add the problem. Sorry for the inconvenience.")

        selectedDays = [dayTable.get(day, "Unknown") for day in self.problem.dows] if self.problem.dows else []
        embed = PositiveEmbed("Problem Days Set", getProblemSentString(self.problem, self.server.settings.timezone))
        if interaction.response.is_done():
            await interaction.followup.send(embed=embed, ephemeral=True)
        else:
            await interaction.response.send_message(embed=embed, ephemeral=True)
        self.server.toJSON()
        

class PremiumSelect(discord.ui.Select):
    def __init__(self, server: Server, problem: Problem, app: App):
        self.server = server
        self.problem = problem
        self.app = app

        options = [
            discord.SelectOption(label="Free", description="Only free problems may be selected", value=0),
            discord.SelectOption(label="Premium", description="Only premium problems may be selected", value=1),
            discord.SelectOption(label="Either", description="Either free or premium problems may be selected", value=2),
        ]
        
        table = { 0: "Free", 1: "Premium", 2: "Either" }
        current = table.get(problem.premium, 0) # default to free if not set
        super().__init__(
            placeholder=f"Select Problem Premium ({current})",
            options=options, min_values=1, max_values=1,
        )

    async def callback(self, interaction: discord.Interaction):
        if len(self.values) != 1:
            await interaction.response.send_message("Invalid selection", ephemeral=True)
            return

        selectedPremium = int(self.values[0])
        self.problem.premium = selectedPremium
        
        match selectedPremium:
            case 0:
                string = "Only **free** problems may be selected"
            case 1:
                string = "Only **premium** problems may be selected"
            case 2:
                string = "Either **free** or **premium** problems may be selected"
            case _:
                string = "Unknown"
        
        embed = PositiveEmbed("Problem Premium Set", string)
        if interaction.response.is_done():
            await interaction.followup.send(embed=embed, ephemeral=True)
        else:
            await interaction.response.send_message(embed=embed, ephemeral=True)

        # since this setting once matters when a problem is selected
        # we don't have to mess with the problem bucket as its at the same time
        self.server.toJSON()
        

class HourSelect(discord.ui.Select):
    def __init__(self, server: Server, problem: Problem, app: App):
        self.server = server
        self.problem = problem
        self.app = app

        # HARD ENCODING B)
        options = [
            discord.SelectOption(label="12 AM", description="Problems will be sent at 12AM + Interval", value=0),
            discord.SelectOption(label="1 AM", description="Problems will be sent at 1AM + Interval", value=1),
            discord.SelectOption(label="2 AM", description="Problems will be sent at 2AM + Interval", value=2),
            discord.SelectOption(label="3 AM", description="Problems will be sent at 3AM + Interval", value=3),
            discord.SelectOption(label="4 AM", description="Problems will be sent at 4AM + Interval", value=4),
            discord.SelectOption(label="5 AM", description="Problems will be sent at 5AM + Interval", value=5),
            discord.SelectOption(label="6 AM", description="Problems will be sent at 6AM + Interval", value=6),
            discord.SelectOption(label="7 AM", description="Problems will be sent at 7AM + Interval", value=7),
            discord.SelectOption(label="8 AM", description="Problems will be sent at 8AM + Interval", value=8),
            discord.SelectOption(label="9 AM", description="Problems will be sent at 9AM + Interval", value=9),
            discord.SelectOption(label="10 AM", description="Problems will be sent at 10AM + Interval", value=10),
            discord.SelectOption(label="11 AM", description="Problems will be sent at 11AM + Interval", value=11),
            discord.SelectOption(label="12 PM", description="Problems will be sent at 12PM + Interval", value=12),
            discord.SelectOption(label="1 PM", description="Problems will be sent at 1PM + Interval", value=13),
            discord.SelectOption(label="2 PM", description="Problems will be sent at 2PM + Interval", value=14),
            discord.SelectOption(label="3 PM", description="Problems will be sent at 3PM + Interval", value=15),
            discord.SelectOption(label="4 PM", description="Problems will be sent at 4PM + Interval", value=16),
            discord.SelectOption(label="5 PM", description="Problems will be sent at 5PM + Interval", value=17),
            discord.SelectOption(label="6 PM", description="Problems will be sent at 6PM + Interval", value=18),
            discord.SelectOption(label="7 PM", description="Problems will be sent at 7PM + Interval", value=19),
            discord.SelectOption(label="8 PM", description="Problems will be sent at 8PM + Interval", value=20),
            discord.SelectOption(label="9 PM", description="Problems will be sent at 9PM + Interval", value=21),
            discord.SelectOption(label="10 PM", description="Problems will be sent at 10PM + Interval", value=22),
            discord.SelectOption(label="11 PM", description="Problems will be sent at 11PM + Interval", value=23),
        ]
        
        self.timezone = self.app.servers[self.problem.serverID].settings.timezone
        tzHour, tzInterval = timeh.convertFromLocalTimeZone(self.problem.hour, self.problem.interval * 15, self.timezone) # convert what we have into our timezone
        
        super().__init__(
            placeholder=f"Select Problem Hour ({tzHour % 12 if tzHour % 12 != 0 else 12} {'AM' if tzHour < 12 else 'PM'})",
            options=options, min_values=1, max_values=1,
        )

    async def callback(self, interaction: discord.Interaction):
        if len(self.values) != 1:
            await interaction.response.send_message("Invalid selection", ephemeral=True)
            return
        
        remove = self.app.synchronizer.removeProblem(self.problem)
        if not remove:
            raise SimpleException("REMOFAIL", "Failed to remove the old problem before setting the new one. This should not happen, please report this issue using `/report`.")
        
        selectedHour = int(self.values[0])

        tzHour, tzInterval = timeh.convertFromLocalTimeZone(self.problem.hour, self.problem.interval * 15, self.timezone) # convert what we have into our timezone
        self.problem.hour, self.problem.interval = timeh.convertToLocalTimeZone(selectedHour, tzInterval * 15, self.timezone) # convert back with the new hour and same interval

        add = self.app.synchronizer.addProblem(self.problem)
        if not add:
            raise SimpleException("ADDAFAIL", "Failed to add the new problem after removing the old one. This should not happen, please report this issue using `/report`.")

        embed = PositiveEmbed("Problem Hour Set", getProblemSentString(self.problem, self.timezone))
        if interaction.response.is_done():
            await interaction.followup.send(embed=embed, ephemeral=True)
        else:
            await interaction.response.send_message(embed=embed, ephemeral=True)

        self.server.toJSON()

class IntervalSelect(discord.ui.Select):
    def __init__(self, server: Server, problem: Problem, app: App):
        self.server = server
        self.problem = problem
        self.app = app

        options = [
            discord.SelectOption(label="0  Min", description="Problems will be sent at hour:00", value=0),
            discord.SelectOption(label="15 Min", description="Problems will be sent at hour:15", value=1),
            discord.SelectOption(label="30 Min", description="Problems will be sent at hour:30", value=2),
            discord.SelectOption(label="45 Min", description="Problems will be sent at hour:45", value=3),
        ]
        
        self.timezone = self.app.servers[self.problem.serverID].settings.timezone
        tzHour, tzInterval = timeh.convertFromLocalTimeZone(self.problem.hour, self.problem.interval * 15, self.timezone)
        
        super().__init__(
            placeholder=f"Select Problem Minute Interval ({tzInterval * 15} Min)",
            options=options, min_values=1, max_values=1,
        )

    async def callback(self, interaction: discord.Interaction):
        if len(self.values) != 1:
            await interaction.response.send_message("Invalid selection", ephemeral=True)
            return
        
        remove = self.app.synchronizer.removeProblem(self.problem)
        if not remove:
            raise SimpleException("REMOFAIL", "Failed to remove the old problem before setting the new one. This should not happen, please report this issue using `/report`.")
        
        selectedInterval = int(self.values[0])
        
        tzHour, tzInterval = timeh.convertFromLocalTimeZone(self.problem.hour, self.problem.interval * 15, self.timezone)
        self.problem.hour, self.problem.interval = timeh.convertToLocalTimeZone(tzHour, selectedInterval * 15, self.timezone)

        add = self.app.synchronizer.addProblem(self.problem)
        if not add:
            raise SimpleException("ADDAFAIL", "Failed to add the new problem after removing the old one. This should not happen, please report this issue using `/report`.")

        embed = PositiveEmbed("Problem Minute Interval Set", getProblemSentString(self.problem, self.timezone))
        if interaction.response.is_done():
            await interaction.followup.send(embed=embed)
        else:
            await interaction.response.send_message(embed=embed)

        self.server.toJSON()