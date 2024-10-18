import discord
from discord import app_commands
from discord.ext import commands

import managers.problem_info_manager as pim
import managers.problem_distrubutor as pmd

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
    async def p(self, interaction: discord.Interaction, difficulty: app_commands.Choice[str], paid: app_commands.Choice[str] = None):
        
        if paid is None:  # set to free by default. allows this to be an optional parameter
            paid = app_commands.Choice(name="Free", value=ps.FREE.value)

        problem = pmd.getProblem(paid.value, difficulty.value)
        problemInfo = pim.getProblemInfo(problem[0])
        
        await interaction.response.send_message(embed = ems.styleProblem(problemInfo, problem[0]))

async def setup(client: commands.Bot) -> None: 
    await client.add_cog(problems(client))