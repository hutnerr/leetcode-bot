import discord
from discord import app_commands
from discord.ext import commands

from models.app import App
from errors.simple_exception import SimpleException
from view.competition_embed import LeaderboardEmbed
from view.error_embed import ErrorEmbed

class CompetitionCog(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client: commands.Bot = client
        self.app: App = client.app
    
    def buildLeaderboard(self, members: list[discord.Member]):
        users = self.app.users
        if not users:
            raise SimpleException("COMPUSERS", "Backend failure")

        board = []
        for member in members:
            if member.id in users:
                # tuple with (points, member)
                memberInfo = (
                    users[member.id].points,
                    member
                )
                board.append(memberInfo)

        board.sort(key=lambda x: x[0], reverse=True) # sort by points
        return board

    # leaderboard
    @app_commands.command(name="leaderboard", description="Displays the current point leaderboard")
    async def leaderboard(self, interaction: discord.Interaction):
        # posts an embed of the entire leaderboard
        boardData = self.buildLeaderboard(interaction.guild.members)
        embed = LeaderboardEmbed(boardData)
        await interaction.response.send_message(embed=embed)

    # rank. gets your rank on the leaderboard
    @app_commands.command(name="rank", description="Displays the point ranking of a specific user")
    async def rank(self, interaction: discord.Interaction, user: discord.User = None):
        # displays a very simple embed of the current rank position of a user
        if user is None:
            user = interaction.user
            
        userID = user.id
        boardData = self.buildLeaderboard(interaction.guild.members)
        
        # look through our data until we find a match
        # once we have we can collect the data and send the msg 
        place = 0
        points = -1
        for data in boardData:
            place += 1
            tempPoints, member = data
            if member.id == userID:
                points = tempPoints
                await interaction.response.send_message(f"**{member.name}** is ranked `{place}`/`{len(boardData)}` with {points} pts")
                return # exit
            
        raise SimpleException("COMPRANK", "User not found in leaderboard", "Make sure the user has completed problems and has points. If this persists, try `/deluser` to reset.")

    # submit pid
    @app_commands.command(name="submit", description="Gives you points if you've completed any active problems")
    async def submit(self, interaction: discord.Interaction):
        # have this just scrape the recent submissions, then use them to check in the servers recent problems
        await interaction.response.send_message("This command is not implemented yet.", ephemeral=True)
    
    @leaderboard.error
    @rank.error
    @submit.error
    async def errorHandler(self, interaction: discord.Interaction, error: app_commands.CommandInvokeError):
        exception: SimpleException = error.original
        code: SimpleException = exception.code if isinstance(error.original, SimpleException) else "BACKEND FAILURE"
        msg = error.original.message if isinstance(error.original, SimpleException) else str(error.original)
        help = error.original.help if isinstance(error.original, SimpleException) else None
        await interaction.response.send_message(embed=ErrorEmbed(code, msg, help), ephemeral=True)

async def setup(client: commands.Bot) -> None: 
    await client.add_cog(CompetitionCog(client))