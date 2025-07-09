import discord.embeds
from models.app import Server
from utils import problem_helper as probh


class ActiveProblemsEmbed(discord.Embed):
    def __init__(self, server: Server):
        super().__init__(title="Active Problems", description="These are the current active problems in the server. If you've completed them, use `/submit` to score some points!\n\n")

        invalidProblems = 0
        for problem in server.activeProblems:
            if not problem[0]:
                invalidProblems += 1
                continue
            self.description += f"> **[{probh.slugToTitle(problem[0])}]({probh.slugToURL(problem[0])})**\n"

        # if we've looked and found 6 problems that aren't invalid
        # then we have no active problems. this is because we have
        # 5 total problems and we skip index 0
        # print(invalidProblems)
        if invalidProblems == 6:
            self.add_field(name="No Active Problems", value="There are no active problems for this server. Active problems will be added when a problem is successfully provided to the server.", inline=False)

        self.color = discord.Color.green()
