import discord.embeds
from models.problem import Problem


class ProblemInfoEmbed(discord.Embed):
    def __init__(self, problems: list[Problem]):
        super().__init__(title="Problem Config Info")
        self.color = discord.Color.blurple()

        problemAdded = False
        for problem in problems:
            if problem is not None:
                self.addProblem(problem)
                problemAdded = True

        if not problemAdded:
            self.description = "There are no problems configured for this server. Use `/pconfig` to add a problem."

        self.set_footer(text="Change the config with /pconfig <ID>. Delete with /delproblem <ID>.")

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
        interval = problem.interval * 15  # convert interval to minutes

        probStr = ""
        amOrPm = "AM" if problem.hour < 12 else "PM"
        hour = problem.hour % 12 if problem.hour != 0 else 12  # convert to 12-hour format
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
