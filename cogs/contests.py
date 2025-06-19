import discord
from discord import app_commands
from discord.ext import commands

from errors.simple_exception import SimpleException
from models.app import App
from services.query_service import QueryService
from utils import time_helper as timeh
from view.contest_embed import ContestEmbed

class Contests(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client: commands.Bot = client
        self.app: App = client.app
        
    @app_commands.command(name = "contests", description = "Gets information about the current LeetCode contests")
    async def contests(self, interaction: discord.Interaction):
        queryService: QueryService = self.app.queryService
        if not queryService:
            raise SimpleException("BACKEND FAILURE")
        
        contestsInfo = queryService.getUpcomingContests()
        if contestsInfo and "data" in contestsInfo:
            upcoming = contestsInfo["data"]["upcomingContests"]
            contests = {}
            for contest in upcoming:
                contests[contest["titleSlug"]] = {
                    "title": contest["title"],
                    "startTime": timeh.formatDateTime(timeh.convertUnixToTime(contest["startTime"])),
                    "timeAway": timeh.formatTimeDelta(timeh.calculateUnixTimeDifference(timeh.getCurrentUNIXTime(), contest["startTime"])),
                    "url": f"https://leetcode.com/contest/{contest['titleSlug']}"
                }
            if contests:
                embed = ContestEmbed(contests)
                await interaction.response.send_message(embed=embed)
        else:
            raise SimpleException("QUERY FAILURE")
            
    @contests.error
    async def errorHandler(self, interaction: discord.Interaction, error: app_commands.CommandInvokeError):
        reportMSG = "Try again later. If you believe this is an issue please submit on GitHub using /report."
        await interaction.response.send_message(f"**{error.original}**: {reportMSG}", ephemeral=True)

async def setup(client: commands.Bot) -> None:
    await client.add_cog(Contests(client))
    