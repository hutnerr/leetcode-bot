import os

import discord
from discord import app_commands
from discord.ext import commands

from errors.simple_exception import SimpleException
from models.app import App
from models.user import User
from services.query_service import QueryService
from utils import file_helper as fileh
from view.confirmation_view import ConfirmationEmbed, ConfirmationView
from view.error_embed import ErrorEmbed
from view.positive_embed import PositiveEmbed
from view.user_info_embed import UserInfoEmbed


class UserCog(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client: commands.Bot = client
        self.app: App = client.app

    @app_commands.command(name = "userinfo", description = "Displays information about a user")
    @app_commands.describe(user="The user to get the info of. Defaults to the user who called the command.")
    async def userinfo(self, interaction: discord.Interaction, user: discord.User = None):
        if user is None: # get self
            user = interaction.user

        userID = user.id
        users = self.app.users

        if userID in users:
            userObj = users[userID]
        else:
            userObj = self.newUser(userID)
                        
        profileInfo = None
        if userObj.leetcodeUsername is not None:
            queryService: QueryService = self.app.queryService
            if not queryService:
                raise SimpleException("UINFOQS", "Backend failure")
            
            # profileInfo = await queryService.getUserProblemsSolved(userObj.leetcodeUsername)
            profileInfo = None
            
            # if not profileInfo or "errors" in profileInfo:
            #     raise SimpleException("UINFOPROFILE", "LeetCode account not found", "Please set your username using `/setusername <username>`")

        embed = UserInfoEmbed(user, userObj, profileInfo)
        await interaction.response.send_message(embed=embed)
    
    
    @app_commands.command(name = "setusername", description = "Set your LeetCode Username")
    async def setusername(self, interaction: discord.Interaction, leetcodeusername: str):
        if leetcodeusername is None or len(leetcodeusername) <= 0:
            raise SimpleException("EMPTY USERNAME")
        
        channel = self.app.servers[interaction.guild.id].settings.postingChannelID
        
        discUser = interaction.user
        userID = discUser.id
        users = self.app.users

        if userID in users:
            user = users[userID]
        else:
            user = self.newUser(userID)

        await interaction.response.defer(ephemeral=True) # defer the response to give us time to process
            
        queryService: QueryService = self.app.queryService
        profileInfo = await queryService.getUserProfile(leetcodeusername)
        
        if "errors" in profileInfo:
            raise SimpleException("USRSETUP", "LeetCode account not found", "Make sure you have a valid LeetCode account and that the username is typed correctly.")

        channel = self.client.get_channel(channel)
        if channel is None:
            raise SimpleException("POSTING_CHANNEL", "Posting channel not found", "Please set the posting channel using `/setpostingchannel <channel>` before setting your username.")
        
        await interaction.followup.send(embed=PositiveEmbed("Username Set", f"Your LeetCode username has been set to `{leetcodeusername}`. You can now use `/userinfo` to view your profile."))

        user.setLeetCodeUsername(leetcodeusername)
        # await interaction.response.send_message("Your username has been successfuly set!", ephemeral=True)

    @app_commands.command(name = "deleteuser", description = "Deletes your user profile")
    async def deluser(self, interaction: discord.Interaction):
        confirmationMSG = "User profiles are **NOT** server specific. If you delete it, your points and progress will be lost **entirely**."
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
                    embed = PositiveEmbed("User Profile Deleted", "Your user profile has been deleted successfully. If you wish to use the submission system again, you will need to set your username using `/setusername <username>`.")
                await interaction.followup.send(embed=embed, ephemeral=True)
            else:
                raise SimpleException("USRDEL", "User profile not found", "You do not have a user profile to delete. Create one using `/setusername <username>` to use the submission system.")
        else: # user clicked no
            embed = PositiveEmbed("Successfully Cancelled", "Your user profile deletion has been cancelled!")
            await interaction.followup.send(embed=embed, ephemeral=True)

    
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
    
    
    @userinfo.error
    @setusername.error
    @deluser.error
    async def errorHandler(self, interaction: discord.Interaction, error: app_commands.CommandInvokeError):
        exception: SimpleException = error.original
        code: SimpleException = exception.code if isinstance(error.original, SimpleException) else "BACKEND FAILURE"
        msg = error.original.message if isinstance(error.original, SimpleException) else str(error.original)
        help = error.original.help if isinstance(error.original, SimpleException) else None
        if interaction.response.is_done():
            await interaction.followup.send(embed=ErrorEmbed(code, msg, help), ephemeral=True)
        else:
            await interaction.response.send_message(embed=ErrorEmbed(code, msg, help), ephemeral=True)

    
async def setup(client: commands.Bot) -> None: 
    await client.add_cog(UserCog(client))