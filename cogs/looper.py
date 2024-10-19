""" 
Handles the loops for the bot. There are no active commands. It is all automated. 

Loops:
    - Problems Loop: Sends problems to the appropriate channels at the appropriate times
    - Update Problemset Loop: Updates the problemset every 24 hours
"""
import discord 
from discord import app_commands
from discord.ext import commands, tasks

from managers import loop_manager as lm
from managers import problem_distrubutor as pmd
from managers import server_settings_manager as ssm
from managers import problemset_builder as pm
from managers import problem_setting_manager as psm 
from managers import active_problems_manager as apm

from ui import embed_styler as es

import time

# TODO: Add a looper for daily problems
# TODO: Add a looper for contest alerts

class Looper(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
        self.loop.start()
        self.updateProblemset.start()
        
    # ############################################################
    # Problems Loop 
    # ############################################################

    @tasks.loop(minutes = 1) # minutes = 1
    async def loop(self) -> None:
        """
        The main problems loop. Runs once a minute.
        It checks the day of the week and the hour of the day and sends problems to the appropriate channels.
        """
        dow = str(time.strftime('%A'))
        hour = int(time.strftime('%H'))

        problems = lm.getAllProblems(dow, hour)
        await self.sendProblems(problems)

    @loop.before_loop
    async def before_loop(self) -> None:
        """
        Setup for the loop. Waits until the bot is ready before starting the loop.
        """
        await self.client.wait_until_ready()

    async def sendProblems(self, problems: list) -> None:
        """
        Iterates over the problems that need to be sent and sends them out
        Args:
            problems (list): The problems to send. Each problem is a string in the format serverID-problemNum
        """
        for problem in problems:
            serverID, problemNum = problem.split("-") # serverID-problemNum
            problem = pmd.getProblemFromSettings(serverID, problemNum) 
            channelID = ssm.getChannelToSendTo(serverID)
            channel = self.client.get_channel(channelID)
            problemSlug = problem[0]
            
            if channel is None:
                print(f"Error: Could not find channel with ID {channelID}")
                return
        
            # This try catch is here because some problems are too long to send in an embed and will throw an error
            try:
                await channel.send(embed = es.styleProblem(psm.getProblemInfo(problemSlug), problemSlug))
            except Exception as e:
                print(e)
                await channel.send(embed = es.styleProblemSimple(psm.getProblemInfo(problemSlug), problemSlug))
                                
            # We need to keep track of what problems are active in the server
            apm.updateActiveProblems(serverID, problemNum, problem[0]) 
    
    # ############################################################
    # Update Problemset Loop
    # ############################################################

    @tasks.loop(hours = 24)
    async def updateProblemset(self):
        """
        Updates the problemset every 24 hours
        """
        pm.scrapeAndBuild()
    
    @updateProblemset.before_loop
    async def before_updateProblemset(self):
        """
        Setup for the loop. Waits until the bot is ready before starting the loop.
        """
        await self.client.wait_until_ready()

# ############################################################
# Setup Below
# ############################################################

async def setup(client: commands.Bot) -> None: 
    """
    Adds the submitter cog to the client
    Args:
        client (commands.Bot): Our bot client
    """
    await client.add_cog(Looper(client))