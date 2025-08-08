import discord
from discord import app_commands
from discord.ext import commands

from errors.simple_exception import SimpleException
from models.app import App
from models.user import User
from view.competition_embed import LeaderboardEmbed
from view.error_embed import ErrorEmbed
from view.positive_embed import PositiveEmbed


class CompetitionCog(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client: commands.Bot = client
        self.app: App = client.app
    
    def buildLeaderboard(self, members: list[discord.Member]):
        users = self.app.users

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
    @app_commands.describe(user="The user to get the rank of. Defaults to the user who called the command.")
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
                await interaction.response.send_message(embed=PositiveEmbed("Rank Information", f"**{member.name}** is ranked `{place}`/`{len(boardData)}` with **{points} pts**", thumbnail=member.display_avatar.url))
                return # exit
            
        raise SimpleException("COMPRANK", "User not found in leaderboard", "Make sure the user has completed problems and has points. If this persists, try `/deluser` to reset.")

    # submit pid
    @app_commands.command(name="submitproblems", description="Gives you points if you've completed any active problems")
    async def submit(self, interaction: discord.Interaction):
        # have this just scrape the recent submissions, then use them to check in the servers recent problems
        userID = interaction.user.id
        if userID not in self.app.users:
            # new  user
            user = User(discordID=userID)
            self.app.users[user.discordID] = user
            user.toJSON() # save the new user
        else:
            user = self.app.users[userID]
            
        prevPoints = user.points
            
        if user.leetcodeUsername is None:
            raise SimpleException("LEETCODEUSER", "You have not set your LeetCode username. Use `/setleetcode` to set it.", "Make sure you have a LeetCode account and that you have completed problems.")

        await interaction.response.defer(thinking=True)  # defer the response to avoid timeout
        submitted = await self.app.submitter.submit(interaction.guild.id, userID)
        if not submitted:
            raise SimpleException("SUBMITFAIL", "You have not completed any active problems or you have already submitted them.", "Make sure you have completed problems and that they are active on the server. If this persists, try `/deluser` to reset your user data.")

        if user.points == prevPoints:
            raise SimpleException("NOPOINTS", "You have not completed any new problems since your last submission.", "Make sure you have completed new problems that are active on the server (check using `/pactive`). If this persists, try `/deluser` to reset your user data.")
        else:
            await interaction.followup.send(embed=PositiveEmbed("Submission Completed", f"Successfully submitted your problems! You now have **{user.points} points**. You went up **{user.points - prevPoints} points**!"), ephemeral=True)

    @leaderboard.error
    @rank.error
    @submit.error
    async def errorHandler(self, interaction: discord.Interaction, error: app_commands.CommandInvokeError):
        exception: SimpleException = error.original
        code: SimpleException = exception.code if isinstance(error.original, SimpleException) else "BACKEND FAILURE"
        msg = error.original.message if isinstance(error.original, SimpleException) else str(error.original)
        help = error.original.help if isinstance(error.original, SimpleException) else None
        if interaction.response.is_done():
            await self.client.sendErrAlert(f"Error in {interaction.command.name} command: {msg}")
            await interaction.followup.send(embed=ErrorEmbed(code, msg, help), ephemeral=True)
        else:
            await self.client.sendErrAlert(f"Error in {interaction.command.name} command: {msg}")
            await interaction.response.send_message(embed=ErrorEmbed(code, msg, help), ephemeral=True)

async def setup(client: commands.Bot) -> None: 
    await client.add_cog(CompetitionCog(client))