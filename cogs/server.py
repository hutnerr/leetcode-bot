import os
import discord
from discord import app_commands
from discord.ext import commands

from models.app import App
from models.server import Server
from models.problem import Problem
from models.server_settings import ServerSettings

from errors.simple_exception import SimpleException
from utils import file_helper as fileh

from view.confirmation_view import ConfirmationView, ConfirmationEmbed
from view.server_config_view import ServerConfigView
from view.server_info_embed import ServerInfoEmbed
from view.error_embed import ErrorEmbed
from view.active_problems_embed import ActiveProblemsEmbed
from view.problem_info_embed import ProblemInfoEmbed
from view.problem_config_view import ProblemConfigView

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
        try:
            await interaction.response.send_message(view=ServerConfigView(server, self.app, setting.value), ephemeral=True)
        except Exception as e:
            raise SimpleException("BACKEND FAILURE", "Failed to load server config view", "There was an error loading the server config view. Please try again later.") from e
    
    # sinfo - display the settings
    @app_commands.command(name="sinfo", description="Displays the servers config")
    async def sinfo(self, interaction: discord.Interaction):
        server = self.getServer(interaction)
        await interaction.response.send_message(embed=ServerInfoEmbed(server, interaction.guild))
    
    # pconfig <pid> - change a problem config  
    # When allowing the problem settings to be selected, allow them to select the timezone of the problem.
    # Before it is sent back and saved, convert it to EST (since that is where I'm at)
    @app_commands.command(name="pconfig", description="Change a problem's settings")
    @app_commands.checks.has_permissions(administrator=True) # only admins can change the server settings
    @app_commands.choices(pids = [
            app_commands.Choice(name=1, value=1),
            app_commands.Choice(name=2, value=2),
            app_commands.Choice(name=3, value=3),
            app_commands.Choice(name=4, value=4),
            app_commands.Choice(name=5, value=5),
        ])
    async def pconfig(self, interaction: discord.Interaction, pids: discord.app_commands.Choice[int]):
        server = self.getServer(interaction)
        
        # if the timezone is not set, then we need to ask the user to set it
        if server.settings.timezone is None:
            raise SimpleException("TIMEZONE", "Timezone not set", "The server's timezone is not set. Please set it using `/sconfig <Other Settings>` before configuring problems. This ensures time accuracy.")

        if server.problems[pids.value] is None:
            embed = ConfirmationEmbed("This problem does not exist. Would you like to create one with default parameters? If created, this problem will begin to run at it's set times.")
            view = ConfirmationView()
            
            if interaction.response.is_done():
                await interaction.followup.send(embed=embed, view=view, ephemeral=True)
            else:
                await interaction.response.send_message(embed=embed, view=view, ephemeral=True)
            if await view.wait():
                raise SimpleException("TIMEOUT", "Problem creation timed out", "The problem creation request timed out. Please try again.")

            if not view.result:  # user clicked no
                await interaction.followup.send("Problem configuration cancelled.", ephemeral=True)
                return
                        
            # user clicked yes, so we will create a new problem
            problem = Problem(
                    pid=pids.value,
                    sid=server.serverID,
                    difs="easy-medium-hard",  # default difficulties
                    dows=[0, 1, 2, 3, 4, 5, 6],  # default days of the week (all)
                    hour=0,  # default hour
                    interval=0,  # default interval
                    premium=0  # default premium
                ) 
            self.app.synchronizer.addProblem(problem)
            
        else:
            problem = server.problems[pids.value]
            if problem is None:
                raise SimpleException("PROBNOTFOUND", "Problem not found", "The problem you are trying to configure does not exist in the server's config. Use `/pinfo` to see the current problems and their configs.")
                
        view=ProblemConfigView(server, problem, self.app)
        if interaction.response.is_done():
            await interaction.followup.send(view=view, ephemeral=True)
        else:
            await interaction.response.send_message(view=view, ephemeral=True)

    # pinfo - display the problem info
    @app_commands.command(name="pinfo", description="Displays a problems info")
    async def pinfo(self, interaction: discord.Interaction):
        server = self.getServer(interaction)
        await interaction.response.send_message(embed=ProblemInfoEmbed(server.problems))
    
    # pactive - display the problems
    @app_commands.command(name="pactive", description="Displays the current active problems")
    async def pactive(self, interaction: discord.Interaction):
        server = self.getServer(interaction)
        await interaction.response.send_message(embed=ActiveProblemsEmbed(server))

    @app_commands.command(name="delproblem", description="Deletes a problem from the server's config")
    @app_commands.checks.has_permissions(administrator=True) # only admins can change the server settings
    @app_commands.choices(pids = [
            app_commands.Choice(name=1, value=1),
            app_commands.Choice(name=2, value=2),
            app_commands.Choice(name=3, value=3),
            app_commands.Choice(name=4, value=4),
            app_commands.Choice(name=5, value=5),
        ])
    @app_commands.describe(pids="The problem ID to delete")
    async def delproblem(self, interaction: discord.Interaction, pids: discord.app_commands.Choice[int]):
        server: Server = self.getServer(interaction)

        problemToRemove = server.problems[pids.value]
        if problemToRemove is None:
            raise SimpleException("PROBNOTFOUND", "Problem not found", "The problem you are trying to delete does not exist in the server's config. Use `/pinfo` to see the current problems and their configs.")
        
        if not self.app.synchronizer.removeProblem(problemToRemove):
            raise SimpleException("PROBDEL", "Failed to delete problem", "The problem could not be deleted. It may not exist or there was an error in the backend.")

        server.toJSON()  # save the server
        await interaction.response.send_message(f"Problem with ID `{pids.value}` has been deleted successfully.", ephemeral=True)
    
    # setchannel - set the channel for the bot to post in
    # @app_commands.command(name="setchannel", description="Sets the bot's output feed channel")
    # @app_commands.checks.has_permissions(administrator=True) # only admins can change the server settings
    # async def setchannel(self, interaction: discord.Interaction, channel: discord.TextChannel = None):
    #     if channel is None:
    #         channel = interaction.channel # if no channel is specified, use the current channel
            
    #     server = self.getServer(interaction)
    #     server.settings.postingChannelID = channel.id # set the channel id
    #     server.toJSON()
    #     await interaction.response.send_message(f"Bot's output feed channel has been set to {channel.mention}", ephemeral=True)
        
    # resetduplicates
    @app_commands.command(name="resetdupes", description="Reset the stored duplicate problems")
    @app_commands.checks.has_permissions(administrator=True) # only admins can change the server settings
    async def resetdupes(self, interaction: discord.Interaction):
        confirmationMSG = "Are you sure you want to reset the stored duplicate problems? This action cannot be undone."
        embed: discord.Embed = ConfirmationEmbed(confirmationMSG)
        view: discord.ui.View = ConfirmationView()
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)
        await view.wait()
        if view.is_finished() and view.result is None:
            await interaction.followup.send("Timed out. Please try again.", ephemeral=True)
            return
    
        if view.result: # user clicked yes
            server: Server = self.getServer(interaction)
            server.previousProblems = [] # reset the previous problems
            server.toJSON() # save the server
            await interaction.followup.send("Stored duplicate problems have been reset successfully.", ephemeral=True)
        else: # user clicked no
            await interaction.followup.send("Duplicate problem deletion cancelled.", ephemeral=True)

    # deleteserver - delete the server config. admin only 
    @app_commands.command(name="delserver", description="Deletes the server configuration")
    @app_commands.checks.has_permissions(administrator=True) # only admins can change the server settings
    async def delserver(self, interaction: discord.Interaction):
        confirmationMSG = "Are you sure you want to delete the server configuration? This action cannot be undone."
        embed: discord.Embed = ConfirmationEmbed(confirmationMSG)
        view: discord.ui.View = ConfirmationView()
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)
        await view.wait()
        if view.is_finished() and view.result is None:
            await interaction.followup.send("Timed out. Please try again.", ephemeral=True)
            return
    
        if not view.result:  # user clicked no
            await interaction.followup.send("Server configuration deletion cancelled.", ephemeral=True)
            return

        server: Server = self.getServer(interaction)
        if server.serverID not in self.app.servers:
            raise SimpleException("SRVDEL", "Server configuration not found", "The server configuration does not exist. It may have already been deleted.")

        del self.app.servers[server.serverID]  # delete the server from the dict
        server.toJSON()  # save the server
        path = os.path.join("data", "servers", f"{server.serverID}.json")
        if fileh.fileExists(path):
            if fileh.deleteFile(path):
                await interaction.followup.send("Server configuration has been deleted successfully.", ephemeral=True)
            else:
                raise SimpleException("SRVDEL", "Failed to delete server configuration file")
            
        
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
    @pactive.error
    @resetdupes.error
    @delserver.error
    @delproblem.error
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
    await client.add_cog(ServerCog(client))