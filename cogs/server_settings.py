# remember to perform admin checks on the setting commands 



# TODO: 
# /toggleroles command
# change if you want the server to have roles that get @ messages. 
# create and assign them when toggled initially. if toggled off delete the roles. 
# perform an admin check, same as settings. since creating roles probably needs admin, 
# make this command perform a self admin check, if it doesnt have it, give an ephemeral 
# back that says give me admin pls so i can do this. 

# /sinfo 
# - displays the servers current config settings
# - displays how many people in the server are opted in

# /setchannel
# - sets the channel for the bot to send messages to.

# /setproblems
# provides the more advanced element that allows the user to modify the server problems 

# /settings <setting>
# can either specifiy a setting for a specific one
# or dont and it'll list the ui elements to change them all

import discord 
from discord import app_commands
from discord.ext import commands

from managers import server_settings_manager as ssm

from ui import embed_styler as ems 

def getTimezones() -> list[app_commands.Choice[str]]:
    """
    Returns a list of timezones for the discord command
    Returns:
        list[app_commands.Choice[str]]: A list of timezones
    """
    timezones = [
            # https://www.worldtimezone.com/
            # TODO: Fill out these timezone equiavlents
            app_commands.Choice(name = "(UTC-12)", value = "UTC-12"),
            app_commands.Choice(name = "(UTC-11)", value = "UTC-11"),
            app_commands.Choice(name = "UTC-10", value = "UTC-10"),
            app_commands.Choice(name = "UTC-9", value = "UTC-9"),
            app_commands.Choice(name = "UTC-8", value = "UTC-8"),
            app_commands.Choice(name = "UTC-7", value = "UTC-7"),
            app_commands.Choice(name = "UTC-6", value = "UTC-6"),
            app_commands.Choice(name = "UTC-5", value = "UTC-5"),
            app_commands.Choice(name = "UTC-4", value = "UTC-4"),
            app_commands.Choice(name = "UTC-3", value = "UTC-3"),
            app_commands.Choice(name = "UTC-2", value = "UTC-2"),
            app_commands.Choice(name = "UTC-1", value = "UTC-1"),
            app_commands.Choice(name = "UTC", value = "UTC"),
            app_commands.Choice(name = "UTC+1", value = "UTC+1"),
            app_commands.Choice(name = "UTC+2", value = "UTC+2"),
            app_commands.Choice(name = "UTC+3", value = "UTC+3"),
            app_commands.Choice(name = "UTC+4", value = "UTC+4"),
            app_commands.Choice(name = "EST (UTC+5)", value = "UTC+5"),
            app_commands.Choice(name = "UTC+6", value = "UTC+6"),
            app_commands.Choice(name = "UTC+7", value = "UTC+7"),
            app_commands.Choice(name = "UTC+8", value = "UTC+8"),
            app_commands.Choice(name = "UTC+9", value = "UTC+9"),
            app_commands.Choice(name = "UTC+10", value = "UTC+10"),
            app_commands.Choice(name = "UTC+11", value = "UTC+11"),
            app_commands.Choice(name = "UTC+12", value = "UTC+12")
            ]
    return timezones

# FIXME: Make these embeds nice 

class ServerSettings(commands.Cog):

    def __init__(self, client: commands.Bot):
        self.client = client
        
    @app_commands.command(name = "sinfo", description = "Displays the servers current config settings")
    async def sinfo(self, interaction: discord.Interaction) -> None:
        """
        Displays the servers current config settings
        Args:
            interaction (discord.Interaction): The interaction that triggered this command
        """
        try:
            settings = ssm.getAndParseServerSettings(interaction.guild.id)
        except Exception as e:
            settings = None
            
        if settings is None:
            await interaction.response.send_message("This server has not been setup yet.", ephemeral = True)
        else:
            await interaction.response.send_message(f"Server settings are: {settings}", ephemeral = True)
    
    @app_commands.command(name = "serversetup", description = "Initial setup for the server")
    @app_commands.choices(timezone = getTimezones())
    async def serversetup(self, interaction: discord.Interaction, timezone: app_commands.Choice[str]) -> None:
        """
        Initial setup for the server
        Args:
            interaction (discord.Interaction): The interaction that triggered this command
        """
        if ssm.addNewServer(interaction.guild.id, interaction.channel.id, timezone.value):
            await interaction.response.send_message(embed = ems.styleSimpleEmbed("Success!", "You have successfully setup the server.", discord.Color.green()), ephemeral = True)
        else:
            await interaction.response.send_message(embed = ems.styleSimpleEmbed("Failure", "Perhaps you're already setup? \nTry `/sinfo to check`", discord.Color.red()), ephemeral = True)
        
    @app_commands.command(name = "setchannel", description = "Sets the channel for the bot to send messages to this one.")
    async def setchannel(self, interaction: discord.Interaction) -> None:
        """
        Sets the channel for the bot to send messages to.
        Args:
            interaction (discord.Interaction): The interaction that triggered this command
        """
        if ssm.updateServer(interaction.guild.id, "channelID", interaction.channel.id):
            await interaction.response.send_message(embed = ems.styleSimpleEmbed("Success!", "You have successfully set the channel.", discord.Color.green()), ephemeral = True)
        else:
            await interaction.response.send_message(embed = ems.styleSimpleEmbed("Failure", "Perhaps you're not setup? \nTry `/serversetup`", discord.Color.red()), ephemeral = True)
        
    @app_commands.command(name = "settimezone", description = "Sets the timezone for the server")
    @app_commands.choices(timezone = getTimezones())
    async def settimezone(self, interaction: discord.Interaction, timezone: app_commands.Choice[str]) -> None:
        """
        Sets the timezone for the server
        Args:
            interaction (discord.Interaction): The interaction that triggered this command
            timezone (app_commands.Choice[str]): The timezone to set
        """
        if ssm.updateServer(interaction.guild.id, "timezone", timezone.value):
            await interaction.response.send_message(embed = ems.styleSimpleEmbed("Success!", "You have successfully set the timezone.", discord.Color.green()), ephemeral = True)
        else:
            await interaction.response.send_message(embed = ems.styleSimpleEmbed("Failure", "Perhaps you're not setup? \nTry `/serversetup`", discord.Color.red()), ephemeral = True)
    
async def setup(client: commands.Bot) -> None: 
    """
    Adds the submitter cog to the client
    Args:
        client (commands.Bot): Our bot client
    """
    await client.add_cog(ServerSettings(client))