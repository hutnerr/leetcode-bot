"""
Cog for handling user settings

Discord Commands:
    - usersetup: Sets up the user to participate
    - uinfo: Displays the users current settings
    - leetcodeusername: Changes the users LeetCode username
"""
import discord 
from discord import app_commands
from discord.ext import commands

from managers import user_setting_manager as usm 

from ui import embed_styler as ems 

class UserSettings(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
        
    @app_commands.command(name = "usersetup", description = "Sets up the user to participate")
    async def usersetup(self, interaction: discord.Interaction, lcusername:str) -> None:
        """
        Sets up the user to participate
        Args:
            interaction (discord.Interaction): The interaction that triggered this command
        """
        if usm.addNewUser(interaction.user.id, lcusername, interaction.guild.id):
            await interaction.response.send_message(embed = ems.styleSimpleEmbed("Success!", "You have successfully been setup to participate.", discord.Color.green()), ephemeral = True)
        else:
            await interaction.response.send_message(embed = ems.styleSimpleEmbed("Failure", "Perhaps you're already setup? \nTry `/uinfo to check`", discord.Color.red()), ephemeral = True)
        
    @app_commands.command(name = "uinfo", description = "Displays the users current settings")
    async def uinfo(self, interaction: discord.Interaction) -> None:
        """
        Displays the users current settings
        Args:
            interaction (discord.Interaction): The interaction that triggered this command
        """
        # FIXME: Pass this to a fancy embed 
        userSettings = usm.getUserSettings(interaction.user.id)
        await interaction.response.send_message(f"Your current settings are: {userSettings}")
        
    @app_commands.command(name = "leetcodeusername", description = "Changes the users LeetCode username")
    async def leetcodeusername(self, interaction: discord.Interaction, lcusername:str) -> None:
        """
        Changes the users LeetCode username
        Args:
            interaction (discord.Interaction): The interaction that triggered this command
        """
        if usm.changeLeetcodeUsername(interaction.user.id, lcusername):
            await interaction.response.send_message(embed = ems.styleSimpleEmbed("Success", "Your LeetCode username has been updated!", discord.Color.green()), ephemeral = True)
        else:
            await interaction.response.send_message(embed = ems.styleSimpleEmbed("Failure", "Perhaps you're not setup? \nTry `/usersetup <leetcodeusername>`", discord.Color.red()), ephemeral = True)
        
    # TODO: Add the opt command 
    
async def setup(client: commands.Bot) -> None: 
    """
    Adds the submitter cog to the client
    Args:
        client (commands.Bot): Our bot client
    """
    await client.add_cog(UserSettings(client))