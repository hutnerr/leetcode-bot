import discord
from discord import app_commands
from discord.ext import commands

from errors.simple_exception import SimpleException
from models.app import App
from services.query_service import QueryService
from utils import datetime_helper as timeh
from view.contest_embed import ContestEmbed
from view.error_embed import ErrorEmbed

class Contests(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client: commands.Bot = client
        self.app: App = client.app
    
    @app_commands.command(name = "contests", description = "Gets information about the current LeetCode contests")
    async def contests(self, interaction: discord.Interaction):
        queryService: QueryService = self.app.queryService
        if not queryService:
            raise SimpleException("CONTSQS", "Backend failure")
        
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
            raise SimpleException("CONTSQS", "API Failure")
            
    @contests.error
    async def errorHandler(self, interaction: discord.Interaction, error: app_commands.CommandInvokeError):
        exception: SimpleException = error.original
        code: SimpleException = exception.code if isinstance(error.original, SimpleException) else "BACKEND FAILURE"
        msg = error.original.message if isinstance(error.original, SimpleException) else str(error.original)
        help = error.original.help if isinstance(error.original, SimpleException) else None
        await interaction.response.send_message(embed=ErrorEmbed(code, msg, help), ephemeral=True)

async def setup(client: commands.Bot) -> None:
    await client.add_cog(Contests(client))
    