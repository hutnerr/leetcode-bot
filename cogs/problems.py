import discord
from discord import app_commands
from discord.ext import commands

from errors.simple_exception import SimpleException
from models.app import App
from models.problem import Problem
from services.cache_service import CacheService
from services.problem_service import ProblemService
from services.query_service import QueryService
from view.error_embed import ErrorEmbed
from view.problem_embed import ProblemEmbed


# related to simply getting and producing problems
class Problems(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client: commands.Bot = client
        self.app: App = client.app

    @app_commands.command(name = "lcproblem", description = "Gets a LeeetCode problem. Default is free problems")
    @app_commands.choices(difficulty = [
        app_commands.Choice(name = "Easy", value = "easy"),
        app_commands.Choice(name = "Medium", value = "medium"),
        app_commands.Choice(name = "Hard", value = "hard"),
        app_commands.Choice(name = "Random", value = "easy-medium-hard")])
    @app_commands.choices(paid = [
        app_commands.Choice(name = "Free", value = 0),
        app_commands.Choice(name = "Paid", value = 1),
        app_commands.Choice(name = "All", value = 2)])
    @app_commands.describe(difficulty="The difficulty of the problem", paid="Whether the problem is free or paid")
    async def problem(self, interaction: discord.Interaction, difficulty: app_commands.Choice[str], paid: app_commands.Choice[int] = None) -> None:
        if paid is None:
            premium = 0 # default to free problems
        else:
            premium = paid.value
            
        problemService: ProblemService = self.app.problemService
        if not problemService:
            raise SimpleException("PPROB", "Backend failure")

        # build a Problem object, we can ignore most of its attributes
        # we only need the difficulties and premium
        problem = Problem(pid=-1, sid=-1, dows=[-1], hour=-1, interval=-1,
            difs=difficulty.value,
            premium=premium
        )
        
        await interaction.response.defer(thinking=True)  # defer the response to avoid timeout
        slug, dif = problemService.selectProblem(problem)
        problemInfo = await self.getProblemInfo(slug)
        embed = ProblemEmbed(slug, problemInfo)
        await interaction.followup.send(embed=embed)

    @app_commands.command(name = "dailylcproblem", description = "Gets the LeeetCode daily problem")
    async def dailyproblem(self, interaction: discord.Interaction):
        queryService: QueryService = self.app.queryService
        if not queryService:
            raise SimpleException("PPROBDP", "Backend failure")

        dailyProblem = await queryService.getDailyProblem()
        if dailyProblem and "data" in dailyProblem:
            dailyProblemSlug = dailyProblem["data"]["challenge"]["question"]["titleSlug"]
            await interaction.response.defer(thinking=True)  # defer the response to avoid timeout
            problemInfo = await self.getProblemInfo(dailyProblemSlug)
            embed = ProblemEmbed(dailyProblemSlug, problemInfo)
            await interaction.followup.send(embed=embed)
        else:
            raise SimpleException("PPROBDPQ", "API failure")

    # gets a problem dict info from the cache or from a query
    async def getProblemInfo(self, slug: str) -> dict | None:
        cacheService: CacheService = self.app.cacheService
        queryService: QueryService = self.app.queryService
        
        if not cacheService or not queryService:
            raise SimpleException("PPROBDPINF", "Backend failure")

        # get from the cache if we have it, otherwise do a query and cache the result
        if cacheService.existsInCache(slug):
            problemInfo = cacheService.getFromCache(slug)
        else:
            problemInfo = await queryService.getQuestionInfo(slug)
            if not problemInfo:
                raise SimpleException("PPROBDPQ", "API failure")
            cacheService.cacheProblem(problemInfo)

        if not problemInfo:
            raise SimpleException("PPROBDPINF", "Backend failure")
        
        return problemInfo
    
    @problem.error
    @dailyproblem.error
    async def errorHandler(self, interaction: discord.Interaction, error: app_commands.CommandInvokeError):
        exception: SimpleException = error.original
        code: SimpleException = exception.code if isinstance(error.original, SimpleException) else "BACKEND FAILURE"
        msg = error.original.message if isinstance(error.original, SimpleException) else str(error.original)
        help = error.original.help if isinstance(error.original, SimpleException) else None
        await self.client.sendErrAlert(f"Error in {interaction.command.name} command: {msg}")
        await interaction.response.send_message(embed=ErrorEmbed(code, msg, help), ephemeral=True)

async def setup(client: commands.Bot) -> None: 
    await client.add_cog(Problems(client))