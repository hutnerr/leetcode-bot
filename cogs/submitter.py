import discord
from discord import app_commands
from discord.ext import commands

from tools import image_helper as ih

from managers import user_activity_manager as uam
from managers import active_problems_manager as apm
from managers import problem_info_manager as pim
from managers import daily_problem_manager as dpm

from ui import embed_styler as es

class submitter(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
        
    @app_commands.command(name = "submit", description = "Submits a solution to a problem")
    @app_commands.choices(problem = [
        app_commands.Choice(name = "Official Daily", value = "daily"),
        app_commands.Choice(name = "Problem 1", value = "p1"), 
        app_commands.Choice(name = "Problem 2", value = "p2"), 
        app_commands.Choice(name = "Problem 3", value = "p3"),])
    async def submit(self, interaction: discord.Interaction, problem: app_commands.Choice[str]):
        
        if problem.value == "daily":
            slug = dpm.getOfficialDailyProblemSlug()
        else:        
            activeProblems = apm.getAndParseActiveProblems(interaction.guild.id)
            slug = activeProblems[problem.value]
        # recentlySolved = uam.checkIfRecentlySolved(interaction.user.id, "article-views-i") # for testing

        recentlySolved = uam.checkIfRecentlySolved(interaction.user.id, slug)        
        problemInfo = pim.getProblemInfo(slug)
        
        # Eventually I want this to become a friendly comp between users
        # problem is that submissions must be unique and not repeatable so you can't get infinite points 
        # need to keep track of what gets submitted. maybe unique problems submitted?
        
        if recentlySolved:
            successImage = ih.getRandomThumbsUpImage() # gets a filepath
            em = es.styleSimpleEmbed("Success!", f"You have solved problem: {problemInfo['title']}", discord.Color.green())
            file = discord.File(successImage, filename = "success.png")
            em.set_image(url = "attachment://success.png")
            await interaction.response.send_message(embed = em, file = file)
        else:
            await interaction.response.send_message(embed = es.styleSimpleEmbed("Rejection!", f"You have not solved **{problem.name}**: [{problemInfo['title']}]({problemInfo['url']})\nYou can use `/checkactive` to see which problems are active.\nIf you think there is an error, check your user settings for your LeetCode username.", discord.Color.red()))
        
async def setup(client: commands.Bot) -> None: 
    await client.add_cog(submitter(client))