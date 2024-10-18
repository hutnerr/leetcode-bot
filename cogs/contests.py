import discord
from discord import app_commands
from discord.ext import commands

from managers import contest_time_manager as ctm

from ui import embed_styler as es

class contests(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
        
    @app_commands.command(name = "contests", description = "Gets information about the current LeetCode contests")
    async def contests(self, interaction: discord.Interaction):
        contestInfo = ctm.getAndParseContestsInfo()
        await interaction.response.send_message(embed = es.styleContest(contestInfo))
        
async def setup(client: commands.Bot) -> None:
    await client.add_cog(contests(client))
    