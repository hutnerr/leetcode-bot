"""
This file contains the problems cog, which is responsible for handling all commands related to problems.

Discord Commands:
    - p: Gets a LeetCode problem
    - checkactive: Checks the active problems for the server
    - daily: Gets the official LeetCode daily problem
"""
import discord
from discord import app_commands
from discord.ext import commands

from managers import problem_setting_manager as psm
from managers import problem_distrubutor as pmd
from managers import active_problems_manager as apm
from managers import daily_problem_manager as dpm

from tools.consts import Problemset as ps
from tools.consts import Difficulty as difs

import ui.embed_styler as ems

class problems(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
        
    @app_commands.command(name = "p", description = "Gets a LeeetCode problem")
    @app_commands.choices(difficulty = [
        app_commands.Choice(name = "Easy", value = difs.EASY.value),
        app_commands.Choice(name = "Medium", value = difs.MEDIUM.value),
        app_commands.Choice(name = "Hard", value = difs.HARD.value),
        app_commands.Choice(name = "Random", value = difs.RANDOM.value)])
    @app_commands.choices(paid = [
        app_commands.Choice(name = "Free", value = ps.FREE.value),
        app_commands.Choice(name = "Paid", value = ps.PAID.value),
        app_commands.Choice(name = "All", value = ps.BOTH.value)])
    async def p(self, interaction: discord.Interaction, difficulty: app_commands.Choice[str], paid: app_commands.Choice[str] = None) -> None:
        """
        Sends a LeetCode problem to the user based on their choices. Namely the dif and if they want paid problems or not.
        Args:
            interaction (discord.Interaction): The interaction that triggered this command
            difficulty (app_commands.Choice[str]): The difficulty of the problem. Easy, Medium, Hard, or Random
            paid (app_commands.Choice[str], optional): The type of problems to include. Defaults to None (becomes Free).
        """
        if paid is None:  # set to free by default. allows this to be an optional parameter
            paid = app_commands.Choice(name = "Free", value = ps.FREE.value)

        problem = pmd.getProblem(paid.value, difficulty.value)
        problemInfo = psm.getProblemInfo(problem[0])
        try:
            await interaction.response.send_message(embed = ems.styleProblem(problemInfo))
        except Exception as e:
            print(e)
            await interaction.response.send_message(embed = ems.styleProblemSimple(problemInfo))

    @app_commands.command(name = "checkactive", description = "Checks the active problems for the server")
    async def checkactive(self, interaction: discord.Interaction) -> None:
        """
        Checks the active problems for the server
        Args:
            interaction (discord.Interaction): The interaction that triggered this command
        """
        activeProblems = apm.getAndParseActiveProblems(interaction.guild.id)
        await interaction.response.send_message(embed = ems.styleActiveProblems(activeProblems))

    @app_commands.command(name = "daily", description = "Gets the official LeetCode daily problem")
    async def daily(self, interaction: discord.Interaction):
        """
        Gets the official LeetCode daily
        Args:
            interaction (discord.Interaction): The interaction that triggered this command
        """
        slug = dpm.getOfficialDailyProblemSlug()
        info = psm.getProblemInfo(slug)
        try:
            await interaction.response.send_message(embed = ems.styleProblem(info, slug))
        except Exception as e:
            print(e)
            await interaction.response.send_message(embed = ems.styleProblemSimple(info, slug))


async def setup(client: commands.Bot) -> None: 
    """
    Adds the submitter cog to the client
    Args:
        client (commands.Bot): Our bot client
    """
    await client.add_cog(problems(client))