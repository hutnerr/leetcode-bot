"""
Discord commands related to contests

Commands:
    - contests: Gets information about the current LeetCode contests
"""
import discord
from discord import app_commands
from discord.ext import commands

from managers import contest_manager as ctm

from ui import embed_styler as es

class Contests(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
        
    @app_commands.command(name = "contests", description = "Gets information about the current LeetCode contests")
    async def contests(self, interaction: discord.Interaction):
        """
        Posts an embed that contains information about the upcoming contest times 
        Args:
            interaction (discord.Interaction): The interaction object that triggered this command
        """
        contestInfo = ctm.getAndParseContestsInfo()
        await interaction.response.send_message(embed = es.styleContest(contestInfo))
        
async def setup(client: commands.Bot) -> None:
    """
    Adds the submitter cog to the client
    Args:
        client (commands.Bot): Our bot client
    """
    await client.add_cog(Contests(client))
    