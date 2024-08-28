import discord
from discord import app_commands
from discord.ext import commands, tasks

from datetime import datetime, timezone

import modules.ProblemTools as pt

import random

######################################################################

class problems(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @app_commands.command(name = "p", description = "Gets a LeeetCode problem")
    @app_commands.choices(difficulty = [
        app_commands.Choice(name = "Easy", value = "1"),
        app_commands.Choice(name = "Medium", value = "2"),
        app_commands.Choice(name = "Hard", value = "3"),
        app_commands.Choice(name = "Random", value = "0")])
    @app_commands.choices(paid = [
        app_commands.Choice(name = "Free", value = "free_problems.csv"),
        app_commands.Choice(name = "Paid", value = "paid_problems.csv"),
        app_commands.Choice(name = "All", value = "all_problems.csv")])
    async def p(self, interaction: discord.Interaction, difficulty: app_commands.Choice[str], paid: app_commands.Choice[str] = None):
        
        if paid is None:  # set to free by default. allows this to be an optional parameter
            paid = app_commands.Choice(name="Free", value="free_problems.csv")

        problem = pt.getProblem(paid.value, difficulty.value)
        await interaction.response.send_message(embed = pt.prettifyProblem(problem))

######################################################################

async def setup(client: commands.Bot) -> None: 
    await client.add_cog(problems(client))
