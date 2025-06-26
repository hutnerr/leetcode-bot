import os
import discord
from discord import app_commands
from discord.ext import commands

from errors.simple_exception import SimpleException
from utils import file_helper as fileh

from services.query_service import QueryService

from models.app import App
from models.user import User

from view.user_info_embed import UserInfoEmbed
from view.confirmation_view import ConfirmationView, ConfirmationEmbed
from view.error_embed import ErrorEmbed

class UserCog(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client: commands.Bot = client
        self.app: App = client.app

    @app_commands.command(name = "uinfo", description = "Displays information about a user")
    async def uinfo(self, interaction: discord.Interaction, user: discord.User = None):
        if user is None: # get self
            user = interaction.user

        userID = user.id
        users = self.app.users
        if not users:
            raise SimpleException("UINFOURS", "Backend failure")

        if userID in users:
            userObj = users[userID]
        else:
            userObj = self.newUser(userID)
                        
        profileInfo = None
        if userObj.leetcodeUsername is not None:
            queryService: QueryService = self.app.queryService
            if not queryService:
                raise SimpleException("UINFOQS", "Backend failure")
            
            profileInfo = queryService.getUserProblemsSolved(userObj.leetcodeUsername)
            
            if "errors" in profileInfo:
                raise SimpleException("UINFOPROFILE", "LeetCode account not found", "Please set your username using `/setusername <username>`")

        embed = UserInfoEmbed(user, userObj, profileInfo)
        await interaction.response.send_message(embed=embed)
    
    
    @app_commands.command(name = "setusername", description = "Set your LeetCode Username")
    async def setusername(self, interaction: discord.Interaction, leetcodeusername: str):
        if leetcodeusername is None or len(leetcodeusername) <= 0:
            raise SimpleException("EMPTY USERNAME")
        
        discUser = interaction.user
        userID = discUser.id
        users = self.app.users
        if not users:
            raise SimpleException("USRSETURS", "Backend failure")
        
        if userID in users:
            user = users[userID]
        else:
            user = self.newUser(userID)
            
        # perform query
        queryService: QueryService = self.app.queryService
        profileInfo = queryService.getUserProfile(leetcodeusername)
        
        if "errors" in profileInfo:
            raise SimpleException("USRSETUP", "LeetCode account not found", "Make sure you have a valid LeetCode account and that the username is typed correctly.")

        user.setLeetCodeUsername(leetcodeusername)
        await interaction.response.send_message("Your username has been successfuly set!", ephemeral=True)        
    
    @app_commands.command(name = "deluser", description = "Deletes your user profile")
    async def deleteuser(self, interaction: discord.Interaction):
        # remove from the dict
        # delete the file
        # send an are you sure embed, say that user profiles are NOT server specific
        confirmationMSG = "User profiles are **NOT** server specific. If you delete it, your progress will be lost **entirely**."
        embed: discord.Embed = ConfirmationEmbed(confirmationMSG)
        view: discord.View = ConfirmationView()
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)
    
        await view.wait()
        if view.is_finished() and view.result is None:
            await interaction.followup.send("Timed out. Please try again.", ephemeral=True)
            return
        
        if view.result: # user clicked yes
            discUser = interaction.user
            userID = discUser.id
            users = self.app.users

            if userID in users:
                del users[userID] # delete from the dict
                path = os.path.join("data", "users", f"{userID}.json")
                if fileh.fileExists(path):
                    fileh.deleteFile(path) # delete the file
                await interaction.followup.send("Your user profile has been deleted successfully.", ephemeral=True)
            else:
                raise SimpleException("USRDEL", "User profile not found", "You do not have a user profile to delete.")
        else: # user clicked no
            await interaction.followup.send("User profile deletion cancelled.", ephemeral=True)

    
    def newUser(self, discID: int) -> User:
        # if the user doesnt exist, then make a blank slate
        user = User(
            discordID=discID,
            leetcodeUsername=None,
            points=0
        )
        self.app.users[discID] = user # add to the dict
        user.toJSON() # save the user
        return user
    
    
    @uinfo.error
    @setusername.error
    @deleteuser.error
    async def errorHandler(self, interaction: discord.Interaction, error: app_commands.CommandInvokeError):
        exception: SimpleException = error.original
        code: SimpleException = exception.code if isinstance(error.original, SimpleException) else "BACKEND FAILURE"
        msg = error.original.message if isinstance(error.original, SimpleException) else str(error.original)
        help = error.original.help if isinstance(error.original, SimpleException) else None
        await interaction.response.send_message(embed=ErrorEmbed(code, msg, help), ephemeral=True)

    
async def setup(client: commands.Bot) -> None: 
    await client.add_cog(UserCog(client))