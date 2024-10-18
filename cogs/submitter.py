import discord
from discord import app_commands
from discord.ext import commands

from tools.consts import Boundaries as bounds
from tools import database_helper as dbh

from managers import user_activity_manager as uam
from managers import server_settings_manager as ssm

def addPossibleProblems():
    problems = []
    
    for i in range(bounds.MIN_PROBLEMS.value + 1, bounds.MAX_PROBLEMS.value + 1):
        problems.append(app_commands.Choice(name = f"Problem {i}", value = i))
    
    return problems

class submitter(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
        
    @app_commands.command(name = "submit", description = "Submits a solution to a problem")
    @app_commands.choices(problem = addPossibleProblems())
    async def submit(self, interaction: discord.Interaction, problem: app_commands.Choice[int]):
        
        # check if the server has a problem with the problem id 
        serverRow = dbh.getRows("problems", "serverID = ?", (interaction.guild.id,))
        numOfServerProblems = ssm.parseServerSettings(serverRow)["problemsNum"]
        
        if (int(numOfServerProblems) < problem.value):
            await interaction.response.send_message(f"Error: Problem {problem.value} does not exist in this server\nYou can recongigure this in the server problem settings")
            return
        
        problemslug = "article-views-i"
        
        recentlySolved = uam.checkIfRecentlySolved(interaction.user.id, problemslug)
        
        if recentlySolved:
            await interaction.response.send_message(f"Success! You have solved problem: {problem.value}")
        else:
            await interaction.response.send_message(f"You have not solved: {problem.value}\nIf you think this is an error, check your user settings for your leetcode username")
        
async def setup(client: commands.Bot) -> None: 
    await client.add_cog(submitter(client))