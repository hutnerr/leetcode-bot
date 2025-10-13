import os

import discord
from discord import app_commands
from discord.ext import commands

from errors.simple_exception import SimpleException
from models.app import App
from models.problem import Problem
from models.server import Server
from models.server_settings import ServerSettings
from utils import file_helper as fileh
from view.active_problems_embed import ActiveProblemsEmbed
from view.confirmation_view import ConfirmationEmbed, ConfirmationView
from view.error_embed import ErrorEmbed
from view.positive_embed import PositiveEmbed
from view.problem_config_view import ProblemConfigView
from view.problem_info_embed import ProblemInfoEmbed
from view.server_config_view import ServerConfigView
from view.server_info_embed import ServerInfoEmbed


class ServerCog(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client: commands.Bot = client
        self.app: App = client.app

    # serverconfig - change the settings
    @app_commands.command(name="serverconfig", description="Configure the servers settings")
    @app_commands.choices(setting = [
        app_commands.Choice(name="Upcoming Contest Alerts", value="upcomingcontests"),
        app_commands.Choice(name="Static Time Alerts", value="staticalerts"),
        app_commands.Choice(name="Other Settings", value="other"),])
    @app_commands.checks.has_permissions(administrator=True) # only admins can change the server settings
    @app_commands.describe(setting="The setting group to configure")
    async def sconfig(self, interaction: discord.Interaction, setting: app_commands.Choice[str]):
        server = self.getServer(interaction)
        try:
            await interaction.response.send_message(view=ServerConfigView(server, self.app, setting.value), ephemeral=True)
        except Exception as e:
            raise SimpleException("BACKEND FAILURE", "Failed to load server config view", "There was an error loading the server config view. Please try again later.") from e

    # serverinfo - display the settings
    @app_commands.command(name="serverinfo", description="Displays the servers config")
    async def sinfo(self, interaction: discord.Interaction):
        server = self.getServer(interaction)
        await interaction.response.send_message(embed=ServerInfoEmbed(server, interaction.guild))
    
    # pconfig <pid> - change a problem config  
    # When allowing the problem settings to be selected, allow them to select the timezone of the problem.
    # Before it is sent back and saved, convert it to EST (since that is where I'm at)
    @app_commands.command(name="problemconfig", description="Change a problem's settings")
    @app_commands.checks.has_permissions(administrator=True) # only admins can change the server settings
    @app_commands.choices(pids = [
            app_commands.Choice(name=1, value=1),
            app_commands.Choice(name=2, value=2),
            app_commands.Choice(name=3, value=3),
            app_commands.Choice(name=4, value=4),
            app_commands.Choice(name=5, value=5),
        ])
    @app_commands.describe(pids="The ID of the problem to configure")
    @app_commands.rename(pids="problemid")
    async def pconfig(self, interaction: discord.Interaction, pids: discord.app_commands.Choice[int]):
        server = self.getServer(interaction)
        
        # if the timezone is not set, then we need to ask the user to set it
        if server.settings.timezone is None:
            raise SimpleException("TIMEZONE", "Timezone not set", "The server's timezone is not set. Please set it using `/serverconfig <Other Settings>` before configuring problems. This ensures time accuracy.")

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
                raise SimpleException("PROBNOTFOUND", "Problem not found", "The problem you are trying to configure does not exist in the server's config. Use `/probleminfo` to see the current problems and their configs.")
                
        view=ProblemConfigView(server, problem, self.app)
        if interaction.response.is_done():
            await interaction.followup.send(view=view, ephemeral=True)
        else:
            await interaction.response.send_message(view=view, ephemeral=True)

    # pinfo - display the problem info
    @app_commands.command(name="probleminfo", description="Displays all configured problem's info")
    async def pinfo(self, interaction: discord.Interaction):
        server = self.getServer(interaction)
        await interaction.response.send_message(embed=ProblemInfoEmbed(server.problems, server))

    # problemactive - display the problems
    @app_commands.command(name="problemactive", description="Displays the current active problems")
    async def pactive(self, interaction: discord.Interaction):
        server = self.getServer(interaction)
        await interaction.response.send_message(embed=ActiveProblemsEmbed(server))

    @app_commands.command(name="deleteproblem", description="Deletes a problem from the server's config")
    @app_commands.checks.has_permissions(administrator=True) # only admins can change the server settings
    @app_commands.choices(pids = [
            app_commands.Choice(name=1, value=1),
            app_commands.Choice(name=2, value=2),
            app_commands.Choice(name=3, value=3),
            app_commands.Choice(name=4, value=4),
            app_commands.Choice(name=5, value=5),
        ])
    @app_commands.describe(pids="The problem ID to delete")
    @app_commands.rename(pids="problemid")
    async def delproblem(self, interaction: discord.Interaction, pids: discord.app_commands.Choice[int]):
        server: Server = self.getServer(interaction)

        problemToRemove = server.problems[pids.value]
        if problemToRemove is None:
            raise SimpleException("PROBNOTFOUND", "Problem not found", "The problem you are trying to delete does not exist in the server's config. Use `/probleminfo` to see the current problems and their configs.")

        if not self.app.synchronizer.removeProblem(problemToRemove):
            raise SimpleException("PROBDEL", "Failed to delete problem", "The problem could not be deleted. It may not exist or there was an error in the backend.")

        server.toJSON()  # save the server
        embed = PositiveEmbed("Problem Deleted", f"Problem with ID `{pids.value}` has been deleted successfully.")
        await interaction.response.send_message(embed=embed, ephemeral=True)

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
            embed = PositiveEmbed("Duplicate Problems Reset", "The stored duplicate problems have been reset successfully.")
            await interaction.followup.send(embed=embed, ephemeral=True)
        else: # user clicked no
            embed = PositiveEmbed("Reset Cancelled", "The duplicate problem reset has been cancelled.")
            await interaction.followup.send(embed=embed, ephemeral=True)

    # deleteserver - delete the server config. admin only 
    @app_commands.command(name="deleteserver", description="Deletes the server configuration entirely")
    @app_commands.checks.has_permissions(administrator=True)  # only admins can change the server settings
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
            embed = PositiveEmbed("Deletion Cancelled", "The server configuration deletion has been cancelled.")
            await interaction.followup.send(embed=embed, ephemeral=True)
            return

        server: Server = self.getServer(interaction)
        if server.serverID not in self.app.servers:
            raise SimpleException("SRVDEL", "Server configuration not found", "The server configuration does not exist. It may have already been deleted.")

        # alerts should only be in the bucket if this setting is enabled
        # otherwise this clears the alert intervals
        if server.settings.contestTimeAlerts:
            if not self.app.synchronizer.changeAlertIntervals(server.serverID, []):  # reset the alert intervals
                raise SimpleException("SRVDEL", "Failed to reset alert intervals", "The alert intervals could not be reset.")

        # remove all problems from server
        for problem in server.problems:
            if problem is not None:
                if not self.app.synchronizer.removeProblem(problem):
                    raise SimpleException("SRVDEL", "Failed to delete problem during server deletion", "The problem could not be deleted. It may not exist or there was an error in the backend.")

        for bucket in self.app.staticTimeBucket.buckets:
            if server.serverID in self.app.staticTimeBucket.buckets[bucket]:
                if not self.app.staticTimeBucket.removeFromBucket(bucket, server.serverID):
                    raise SimpleException("SRVDEL", "Failed to remove server from static time bucket", "The server could not be removed from the static time bucket. It may not exist or there was an error in the backend.")

        del self.app.servers[server.serverID]  # delete the server from the dict
        server.toJSON()  # save the server
        path = os.path.join("data", "servers", f"{server.serverID}.json")
        if fileh.fileExists(path):
            if fileh.deleteFile(path):
                embed = PositiveEmbed("Server Configuration Deleted", "The server configuration has been deleted successfully.")
                await interaction.followup.send(embed=embed, ephemeral=True)
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
        if isinstance(error, discord.app_commands.MissingPermissions):
            await interaction.response.send_message(embed=ErrorEmbed("PERMISSION DENIED", "You do not have permission to use this command. Administrator permission is required.", "---"), ephemeral=True)
            return
        if isinstance(error.original, SimpleException):
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
        else:
            await self.client.sendErrAlert(f"Error in {interaction.command.name} command: {str(error)}")
            if interaction.response.is_done():
                await interaction.followup.send(embed=ErrorEmbed("BACKEND FAILURE", str(error)), ephemeral=True)
            else:
                await interaction.response.send_message(embed=ErrorEmbed("BACKEND FAILURE", str(error)), ephemeral=True)

async def setup(client: commands.Bot) -> None: 
    await client.add_cog(ServerCog(client))