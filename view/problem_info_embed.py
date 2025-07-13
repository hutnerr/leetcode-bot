import discord.embeds
from models.problem import Problem
from models.server import Server
from utils import datetime_helper as timeh

class ProblemInfoEmbed(discord.Embed):
    def __init__(self, problems: list[Problem], server: Server):
        super().__init__(title="Problem Config Info")
        self.color = discord.Color.blurple()
        self.set_footer(text="Change the config with /problemconfig. Delete with /deleteproblem.")
        self.server = server

        helpStr = "There are no problems configured for this server. Use `/problemconfig` to add a problem."

        # set the description to a default message if there is no timezone set then return
        if server.settings.timezone is None:
            self.description = helpStr + " The server's timezone is not set. Please set it using `/serverconfig <Other Settings>` before configuring problems. This ensures time accuracy."
            return

        problemAdded = False
        for problem in problems:
            if problem is not None:
                self.addProblem(problem)
                problemAdded = True

        if not problemAdded:
            self.description = helpStr
            
    def addProblem(self, problem: Problem):

        dowTable = {
            0: "Sunday",
            1: "Monday",
            2: "Tuesday",
            3: "Wednesday",
            4: "Thursday",
            5: "Friday",
            6: "Saturday"
        }

        dows = [dowTable.get(dow, "Unknown") for dow in problem.dows]

        tzHour, tzInterval = timeh.convertFromLocalTimeZone(problem.hour, problem.interval * 15, self.server.settings.timezone)

        interval = tzInterval * 15

        probStr = ""
        amOrPm = "AM" if tzHour < 12 else "PM"
        hour = 12 if tzHour == 0 or tzHour == 12 else tzHour % 12  # convert to 12-hour format
        probStr += f"{hour:02d}:{interval:02d} {amOrPm}"

        self.add_field(
            name=f"Problem {str(problem.problemID).title()} - {probStr}",
            value=f"> **Difficulties**: {', '.join([d.title() for d in problem.difficulties])}\n"
            f"> **Days**: {', '.join([dow.title() for dow in dows])}\n"
            # f"> **Hour**: {str(problem.hour).title()}\n"
            # f"> **Interval**: {str(interval).title()} minutes\n"
            f"> **Premium**: {'Yes' if problem.premium else 'No'}",
            inline=False
        )
