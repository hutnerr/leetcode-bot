import discord
from discord import app_commands
from discord.ext import commands

from models.app import App
from models.server import Server
from models.server_settings import ServerSettings

from errors.simple_exception import SimpleException

from view.confirmation_view import ConfirmationView, ConfirmationEmbed
from view.server_config_view import ServerConfigView
from view.server_info_embed import ServerInfoEmbed

class ServerCog(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client: commands.Bot = client
        self.app: App = client.app
    
    # sconfig - change the settings
    @app_commands.command(name="sconfig", description="Configure the servers settings. Admin only")
    @app_commands.choices(setting = [
        app_commands.Choice(name="Upcoming Contest Alerts", value="upcomingcontests"),
        app_commands.Choice(name="Static Time Alerts", value="staticalerts"),
        app_commands.Choice(name="Other Settings", value="other"),])
    @app_commands.checks.has_permissions(administrator=True) # only admins can change the server settings
    async def sconfig(self, interaction: discord.Interaction, setting: app_commands.Choice[str]):
        server = self.getServer(interaction)
        await interaction.response.send_message(view=ServerConfigView(server, self.app, setting.value), ephemeral=True)
    
    # sinfo - display the settings
    @app_commands.command(name="sinfo", description="Displays the servers config")
    async def sinfo(self, interaction: discord.Interaction):
        server = self.getServer(interaction)
        await interaction.response.send_message(embed=ServerInfoEmbed(server, interaction.guild))
    
    # pconfig <pid> - change a problem config  
    # When allowing the problem settings to be selected, allow them to select the timezone of the problem.
    # Before it is sent back and saved, convert it to EST (since that is where I'm at)
    @app_commands.command(name="pconfig", description="Change a problem's settings")
    async def pconfig(self, interaction: discord.Interaction):
        pass
    
    # pinfo - display the problem info
    @app_commands.command(name="pinfo", description="Displays a problems info")
    async def pinfo(self, interaction: discord.Interaction):
        pass
    
    # activeproblems - display the problems
    @app_commands.command(name="activeproblems", description="Displays the current active problems")
    async def activeproblems(self, interaction: discord.Interaction):
        pass
    
    # setchannel - set the channel for the bot to post in
    @app_commands.command(name="setchannel", description="Sets the bot's output feed channel")
    async def setchannel(self, interaction: discord.Interaction):
        # use the channel select menu
        pass
    
    # setrole - set the role for the bot to use
    @app_commands.command(name="setrole", description="Sets the bot's role to @mention if the mention flag is active")
    async def setrole(self, interaction: discord.Interaction):
        # use the role select menu
        await interaction.response.send_message(view=discord.ui.RoleSelect())
        pass
    
    # resetduplicates
    @app_commands.command(name="resetdupes", description="Reset the stored duplicate problems")
    async def resetdupes(self, interaction: discord.Interaction):
        pass

    # deleteserver - delete the server config. admin only 
    @app_commands.command(name="deleteserver", description="Deletes the server configuration")
    # @app_commands.checks.has_permissions(administrator=True)
    async def deleteserver(self, interaction: discord.Interaction):
        pass
    
    # gets the server or creates a new one if it doesnt yet exist
    def getServer(self, interaction: discord.Interaction) -> Server:
        # make a new server if it doesnt exist
        serverID = interaction.guild_id
        servers = self.app.servers
        if servers is None:
            raise SimpleException("BACKEND FAILURE")
        
        if serverID in servers:
            server = servers[serverID]
        else:
            server = self.newServer(
                serverID = serverID,
                channelID= interaction.channel_id
            )
        return server
    
    # set the channel to whatever settings is first called in on the creation of a new server
    def newServer(self, serverID: int, channelID: int) -> Server:
        # if the server doesnt exist, then make a blank slate with default settings
        # default settings should be non invasive
        server = Server(
           sid=serverID,
           settings=ServerSettings(postingChannelID=channelID),
        )
        self.app.servers[serverID] = server # add to the dict
        server.toJSON() # save the server
        return server

    @sconfig.error
    @sinfo.error
    @pconfig.error
    @pinfo.error
    @activeproblems.error
    @setchannel.error
    @setrole.error
    @resetdupes.error
    @deleteserver.error
    async def errorHandler(self, interaction: discord.Interaction, error: app_commands.CommandInvokeError):
        reportMSG = "Try again later. If you believe this is an issue please submit on GitHub using /report."
        await interaction.response.send_message(f"**{error.original}**: {reportMSG}", ephemeral=True)

    
async def setup(client: commands.Bot) -> None: 
    await client.add_cog(ServerCog(client))