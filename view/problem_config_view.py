import discord

from models.server import Server
from models.app import App
from models.problem import Problem

from errors.simple_exception import SimpleException

class ProblemConfigView(discord.ui.View):
    def __init__(self, server: Server, problem: Problem, app: App):
        super().__init__(timeout=60)    
        self.add_item(DifficultiesSelect(server, problem, app))
        self.add_item(DaysOfWeekSelect(server, problem, app))
        self.add_item(PremiumSelect(server, problem, app))
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
            placeholder=f"Select Problem Difficulty ({', '.join(problem.difficulties) if problem.difficulties else 'None'})",
            options=options, min_values=1, max_values=3,
        )

    async def callback(self, interaction: discord.Interaction):
        if len(self.values) <= 0:
            await interaction.response.send_message("Invalid selection", ephemeral=True)
            return

        selectedDifficulties = self.values
        self.problem.difficulties = selectedDifficulties
        if interaction.response.is_done():
            await interaction.followup.send(f"**Problem difficulty** is now set to {', '.join(selectedDifficulties)}", ephemeral=True)
        else:
            await interaction.response.send_message(f"**Problem difficulty** is now set to {', '.join(selectedDifficulties)}", ephemeral=True)
        self.app.synchronizer.addProblem(self.problem)
        self.server.toJSON()
        self.app.problemBucket.printBucketClean()

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
        self.dayTable = {
            0: "Sunday",
            1: "Monday",
            2: "Tuesday",
            3: "Wednesday",
            4: "Thursday",
            5: "Friday",
            6: "Saturday"
        }
        selectedDays = [self.dayTable.get(day, "Unknown") for day in problem.dows] if problem.dows else []
        super().__init__(
            placeholder=f"Select Problem Days ({', '.join(selectedDays) if selectedDays else 'None'})",
            options=options, min_values=1, max_values=7,
        )

    async def callback(self, interaction: discord.Interaction):
        if len(self.values) <= 0:
            await interaction.response.send_message("Invalid selection", ephemeral=True)
            return
        
        self.app.problemBucket.printBucketClean()
        
        remove = self.app.synchronizer.removeProblem(self.problem)
        if not remove:
            raise SimpleException("REMOFAIL", "Failed to remove the old problem before setting the new one. This should not happen, please report this issue using `/report`. Also please `/delproblem` and re-add the problem. Sorry for the inconvenience.")

        selectedDays = self.values
        self.problem.dows = [int(day) for day in selectedDays]

        add = self.app.synchronizer.addProblem(self.problem)
        if not add:
            raise SimpleException("ADDPFAIL", "Failed to add the new problem after setting the days. This should not happen, please report this issue using `/report`. Also please `/delproblem` and re-add the problem. Sorry for the inconvenience.")

        selectedDays = [self.dayTable.get(day, "Unknown") for day in self.problem.dows] if self.problem.dows else []
        if interaction.response.is_done():
            await interaction.followup.send(f"**Problem days** are now set to {', '.join(selectedDays)}", ephemeral=True)
        else:
            await interaction.response.send_message(f"**Problem days** are now set to {', '.join(selectedDays)}", ephemeral=True)        
        self.server.toJSON()
        
        self.app.problemBucket.printBucketClean()


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
                string = "Only free problems may be selected"
            case 1:
                string = "Only premium problems may be selected"
            case 2:
                string = "Either free or premium problems may be selected"
            case _:
                string = "Unknown"
        
        if interaction.response.is_done():
            await interaction.followup.send(string, ephemeral=True)
        else:
            await interaction.response.send_message(string, ephemeral=True)

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
        
        super().__init__(
            placeholder=f"Select Problem Hour ({problem.hour})",
            options=options, min_values=1, max_values=1,
        )

    async def callback(self, interaction: discord.Interaction):
        if len(self.values) != 1:
            await interaction.response.send_message("Invalid selection", ephemeral=True)
            return
        
        self.app.problemBucket.printBucketClean()
        
        remove = self.app.synchronizer.removeProblem(self.problem)
        if not remove:
            raise SimpleException("REMOFAIL", "Failed to remove the old problem before setting the new one. This should not happen, please report this issue using `/report`.")
        
        selectedHour = int(self.values[0])
        self.problem.hour = selectedHour
        
        add = self.app.synchronizer.addProblem(self.problem)
        if not add:
            raise SimpleException("ADDAFAIL", "Failed to add the new problem after removing the old one. This should not happen, please report this issue using `/report`.")

        string = f"**Problem hour** is now set to {selectedHour} ({'AM' if selectedHour < 12 else 'PM'})"
        string += f"\n(Problems will be sent at {self.problem.hour}:{self.problem.interval * 15:02})"
        if interaction.response.is_done():
            await interaction.followup.send(string, ephemeral=True)
        else:
            await interaction.response.send_message(string, ephemeral=True)

        print("------------------------------------")
        self.app.problemBucket.printBucketClean()
        self.server.toJSON()

class IntervalSelect(discord.ui.Select):
    def __init__(self, server: Server, problem: Problem, app: App):
        self.server = server
        self.problem = problem
        self.app = app

        options = [
            discord.SelectOption(label="0  Min", description="Problems will be sent at hour:15", value=0),
            discord.SelectOption(label="15 Min", description="Problems will be sent at hour:30", value=1),
            discord.SelectOption(label="30 Min", description="Problems will be sent at hour:45", value=2),
            discord.SelectOption(label="45 Min", description="Problems will be sent at hour:00", value=3),
        ]
        
        super().__init__(
            placeholder=f"Select Problem Hour ({problem.hour})",
            options=options, min_values=1, max_values=1,
        )

    async def callback(self, interaction: discord.Interaction):
        if len(self.values) != 1:
            await interaction.response.send_message("Invalid selection", ephemeral=True)
            return
        
        self.app.problemBucket.printBucketClean()
        
        remove = self.app.synchronizer.removeProblem(self.problem)
        if not remove:
            raise SimpleException("REMOFAIL", "Failed to remove the old problem before setting the new one. This should not happen, please report this issue using `/report`.")
        
        selectedInterval = int(self.values[0])
        self.problem.interval = selectedInterval
        
        add = self.app.synchronizer.addProblem(self.problem)
        if not add:
            raise SimpleException("ADDAFAIL", "Failed to add the new problem after removing the old one. This should not happen, please report this issue using `/report`.")

        string = f"**Problem Interval** is now set to {selectedInterval} ({'AM' if selectedInterval < 12 else 'PM'})"
        string += f"\n(Problems will be sent at {self.problem.hour}:{self.problem.interval * 15:02})"
        if interaction.response.is_done():
            await interaction.followup.send(string, ephemeral=True)
        else:
            await interaction.response.send_message(string, ephemeral=True)

        print("------------------------------------")
        self.app.problemBucket.printBucketClean()
        self.server.toJSON()