# TODO: 
# /toggleroles command
# change if you want the server to have roles that get @ messages. 
# create and assign them when toggled initially. if toggled off delete the roles. 
# perform an admin check, same as settings. since creating roles probably needs admin, 
# make this command perform a self admin check, if it doesnt have it, give an ephemeral 
# back that says give me admin pls so i can do this. 

# /setproblems
# provides the more advanced element that allows the user to modify the server problems 

# /settings <setting>
# can either specifiy a setting for a specific one
# or dont and it'll list the ui elements to change them all

#TODO: Add the list of methods that are located within this to the top of the file 


import discord 
from discord import app_commands
from discord.ext import commands

from managers import server_settings_manager as ssm
from managers import problem_setting_manager as psm

from ui import embed_styler as ems 
from ui import timezone_selectmenu as tsm

from errors.exceptions import NotAdminError

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

def userIsAdmin(client: discord.Client, serverID: int, userID:int ) -> bool:
    """
    Performs a check to see if a user is admin within a given server

    Args:
        serverID (int): The server to check 
        userID (int): The user to check 

    Returns:
        bool: True if user is admin, false otherwise 
    """
    # return False
    server = discord.utils.get(client.guilds, id = serverID)
    member = discord.utils.get(server.members, id = userID)
    return member.guild_permissions.administrator


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
            await interaction.response.send_message(embed = ems.styleSimpleEmbed("Error", "This server has not been setup yet.", discord.Color.red()), ephemeral = True)
        else:
            await interaction.response.send_message(embed = ems.styleServerInfoEmbed(self.client, settings))
    
    @app_commands.command(name = "serversetup", description = "Initial setup for the server")
    @app_commands.choices(timezone = getTimezones())
    # @app_commands.check(userIsAdmin)
    async def serversetup(self, interaction: discord.Interaction, timezone: app_commands.Choice[str]) -> None:
        """
        Initial setup for the server
        Args:
            interaction (discord.Interaction): The interaction that triggered this command
        """
        if not userIsAdmin(self.client, interaction.guild.id, interaction.user.id):
            # await interaction.response.send_message("You need admin permissions to run this command.", ephemeral=True)
            raise NotAdminError()
        
        successFlag = ssm.addNewServer(interaction.guild.id, interaction.channel.id, timezone.value)

        for i in range(1, 4):
            successFlag = successFlag and psm.addProblem(interaction.guild.id, i, "Monday,Tuesday,Wednesday,Thursday,Friday", 12, "Easy,Medium,Hard", "Free")
        
        if successFlag:
            await interaction.response.send_message(embed = ems.styleSimpleEmbed("Success!", "You have successfully setup the server.", discord.Color.green()), ephemeral = True)
        else:
            await interaction.response.send_message(embed = ems.styleSimpleEmbed("Failure", "Perhaps you're already setup? \nTry `/sinfo to check`\nIf this doesn't work, you can reset the entire config with `/configreset`", discord.Color.red()), ephemeral = True)
        
    @app_commands.command(name = "setchannel", description = "Sets the channel for the bot to send messages to this one.")
    async def setchannel(self, interaction: discord.Interaction) -> None:
        """
        Sets the channel for the bot to send messages to.
        Args:
            interaction (discord.Interaction): The interaction that triggered this command
        """
        if not userIsAdmin(self.client, interaction.guild.id, interaction.user.id):
            # await interaction.response.send_message("You need admin permissions to run this command.", ephemeral=True)
            raise NotAdminError()

        if ssm.updateServer(interaction.guild.id, "channelID", interaction.channel.id):
            await interaction.response.send_message(embed = ems.styleSimpleEmbed("Success!", "You have successfully set the channel.", discord.Color.green()), ephemeral = True)
        else:
            await interaction.response.send_message(embed = ems.styleSimpleEmbed("Failure", "Perhaps you're not setup? \nTry `/serversetup`", discord.Color.red()), ephemeral = True)
        
    @app_commands.command(name = "settimezone", description = "Sets the timezone for the server")
    @app_commands.choices(timezone = getTimezones())
    async def settimezone(self, interaction: discord.Interaction, timezone: app_commands.Choice[str] = None) -> None:
        """
        Sets the timezone for the server
        Args:
            interaction (discord.Interaction): The interaction that triggered this command
            timezone (app_commands.Choice[str]): The timezone to set
        """
        if not userIsAdmin(self.client, interaction.guild.id, interaction.user.id):
            # await interaction.response.send_message("You need admin permissions to run this command.", ephemeral=True)
            raise NotAdminError()

        if timezone is None:
            # TODO: Send the GUI version 
            await interaction.channel.send("Please select a timezone", view = tsm.Timezone())
            # await interaction.response.send_message(view = tsm.Timezone())
        else:
            if ssm.updateServer(interaction.guild.id, "timezone", timezone.value):
                await interaction.response.send_message(embed = ems.styleSimpleEmbed("Success!", "You have successfully set the timezone.", discord.Color.green()), ephemeral = True)
            else:
                await interaction.response.send_message(embed = ems.styleSimpleEmbed("Failure", "Perhaps you're not setup? \nTry `/serversetup`", discord.Color.red()), ephemeral = True)
        
    @app_commands.command(name = "configure", description = "Configures the server settings")
    async def configure(self, interaction: discord.Interaction) -> None:
        """
        Configures the server settings
        Args:
            interaction (discord.Interaction): The interaction that triggered this command
        """
        pass

    @app_commands.command(name = "editproblem", description = "Edits a server problems")
    @app_commands.choices(problem = [
        app_commands.Choice(name = "Problem 1", value = 1),
        app_commands.Choice(name = "Problem 2", value = 2),
        app_commands.Choice(name = "Problem 3", value = 3),
    ])
    async def editproblem(self, interaction: discord.Interaction, problem: app_commands.Choice[int]) -> None:
        """
        Edits a server problem
        Args:
            interaction (discord.Interaction): The interaction that triggered this command
        """
        if not userIsAdmin(self.client, interaction.guild.id, interaction.user.id):
            raise NotAdminError()
        
        # psm.updateProblem(interaction.guild.id, problem.value, 

    #  Problems
    # - serverID   : int   : The ID of the discord server this goes to 
    # - problemID  : int   : The ID of this problem for the sever. 1 - 3
    # - dow        : str   : String of CSV possible days of week e.g. "Monday,Friday,Tuesday"
    # - hour       : int   : The set hour each day the problem should post. 0 - 23
    # - difficulty : str   : String of CSV possible difs e.g. "Easy,Medium"
    # - premium    : str   : "Free", "Paid", or "Both"

        # psm.updateProblem(interaction.guild.id, problem.value, , )
        pass

    @app_commands.command(name = "pinfo", description = "Gets the info for the server problems")
    async def pinfo(self, interaction: discord.Interaction) -> None:
        """
        Gets the info for the server problems
        Args:
            interaction (discord.Interaction): The interaction that triggered this command
        """
        problems = psm.getAndParseAllProblems(interaction.guild.id)
        
        if len(problems) == 0:
            await interaction.response.send_message(embed = ems.styleSimpleEmbed("Error", "This server has not been setup yet.", discord.Color.red()), ephemeral = True)
        else:
            print(problems)

    @app_commands.command(name = "configreset", description = "Resets the server config")
    async def configreset(self, interaction: discord.Interaction) -> None:
        """
        Resets the server config
        Args:
            interaction (discord.Interaction): The interaction that triggered this command
        """
        if not userIsAdmin(self.client, interaction.guild.id, interaction.user.id):
            raise NotAdminError()
        
        # TODO: Implement this resetServer function
        if ssm.resetServer(interaction.guild.id):
            await interaction.response.send_message(embed = ems.styleSimpleEmbed("Success!", "You have successfully reset the server config.", discord.Color.green()), ephemeral = True)
        else:
            await interaction.response.send_message(embed = ems.styleSimpleEmbed("Failure", "Perhaps you're not setup? \nTry `/serversetup`", discord.Color.red()), ephemeral = True)

    @serversetup.error
    @setchannel.error
    @settimezone.error
    @editproblem.error
    async def errorHandler(self, interaction: discord.Interaction, error: app_commands.CommandInvokeError) -> None:
        """
        Handles errors for all commands.

        Args:
            interaction (discord.Interaction): The interaction that caused the error
            error (Exception): The error that was raised 
        """
        if (type(error.__cause__) == type(NotAdminError())):
            await interaction.response.send_message(embed = ems.styleSimpleEmbed("Admin Required", "You need admin permissions to run this command.", discord.Color.red()), ephemeral = True)
        else:
            await interaction.response.send_message(embed = ems.styleSimpleEmbed("Error", f"Failed to run command.\n`{error}`", discord.Color.red()), ephemeral = True)

async def setup(client: commands.Bot) -> None: 
    """
    Adds the submitter cog to the client
    Args:
        client (commands.Bot): Our bot client
    """
    await client.add_cog(ServerSettings(client))