"""
Discord Cog for submitting solutions to problems

Not entirely used yet, but will be used for a friendly competition between users.

Discord Commands:
    submit - Submits a solution to a problem (low functionality, not fully implemented)
"""
import discord
from discord import app_commands
from discord.ext import commands

from managers import user_setting_manager as usm
from managers import active_problems_manager as apm
from managers import problem_setting_manager as psm 
from managers import daily_problem_manager as dpm

from tools import image_helper as ih
from tools.consts import ImageFolders as imgf

from ui import embed_styler as es

class submitter(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
        
    @app_commands.command(name = "submit", description = "Submits a solution to a problem")
    # currently staticly set to only allow the official daily and the 3 total problems. might change in the future 
    @app_commands.choices(problem = [
        app_commands.Choice(name = "Official Daily", value = "daily"),
        app_commands.Choice(name = "Problem 1", value = "p1"), 
        app_commands.Choice(name = "Problem 2", value = "p2"), 
        app_commands.Choice(name = "Problem 3", value = "p3"),])
    async def submit(self, interaction: discord.Interaction, problem: app_commands.Choice[str]):
        """
        Submits a solution to a problem. 
        Does this by 
            1. checking if the user solved the problem, 2. sending a success or rejection message
        Args:
            interaction (discord.Interaction): The interaction object that triggered the command
            problem (app_commands.Choice[str]): What problem the user is submitting a solution to. Can be "daily", "p1", "p2", or "p3"
        """
        
        if problem.value == "daily":
            slug = dpm.getOfficialDailyProblemSlug()
        else:        
            activeProblems = apm.getAndParseActiveProblems(interaction.guild.id)
            slug = activeProblems[problem.value]

        recentlySolved = usm.checkIfRecentlySolved(interaction.user.id, slug)        
        problemInfo = psm.getProblemInfo(slug)
        
        # Eventually I want this to become a friendly comp between users
        # problem is that submissions must be unique and not repeatable so you can't get infinite points 
        # need to keep track of what gets submitted. maybe unique problems submitted?
        
        # if recentlySolved we want to send an image as well so it has more of a "reward" feel
        if recentlySolved:
            successImage = ih.getRandomImage(imgf.THUMBS_UP.value) # gets a filepath
            em = es.styleSimpleEmbed("Success!", f"You have solved problem: {problemInfo['title']}", discord.Color.green())
            image = discord.File(successImage, filename = "success.png")
            em.set_image(url = "attachment://success.png")
            await interaction.response.send_message(embed = em, file = image)
        else:
            await interaction.response.send_message(embed = es.styleSimpleEmbed("Rejection!", f"You have not solved **{problem.name}**: [{problemInfo['title']}]({problemInfo['url']})\nYou can use `/checkactive` to see which problems are active.\nIf you think there is an error, check your user settings for your LeetCode username.", discord.Color.red()))
        
async def setup(client: commands.Bot) -> None: 
    """
    Adds the submitter cog to the client
    Args:
        client (commands.Bot): Our bot client
    """
    await client.add_cog(submitter(client))