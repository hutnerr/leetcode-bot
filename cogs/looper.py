import discord 
from discord import app_commands
from discord.ext import commands, tasks

from managers import loop_manager as lm
from managers import problem_distrubutor as pmd
from managers import server_settings_manager as ssm
from managers import problem_info_manager as pim
from managers import problemset_manager as pm

from ui import embed_styler as es

import time

class looper(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
        self.loop.start()
        self.updateProblemset.start()
        
    async def performLoop(self):
        # dow = time.strftime('%A')
        # hour = time.strftime('%H')
        
        # for testing 
        dow = '1'
        hour = 1
        
        problems = lm.getAllProblems(dow, hour)
        await self.sendProblems(problems)
        
    @tasks.loop(minutes = 1) # minutes = 1
    async def loop(self):
        await self.performLoop()

    @loop.before_loop
    async def before_loop(self):
        await self.client.wait_until_ready()

    async def sendProblems(self, problems):
        for problem in problems:
            serverID, problemNum = problem.split("-")
            problem = pmd.getProblemsFromSettings(serverID, problemNum)
            channelID = ssm.getChannelToSendTo(serverID)
            
            channel = self.client.get_channel(channelID)
            problemSlug = problem[0]
            
            try:
                await channel.send(embed = es.styleProblem(pim.getProblemInfo(problemSlug), problemSlug))
            except Exception as e:
                await channel.send(embed = es.styleProblemSimple(pim.getProblemInfo(problemSlug), problemSlug))
                                
            pmd.updateActiveProblems(serverID, problemNum, problem[0])
    
    @tasks.loop(hours=24)
    async def updateProblemset(self):
        pm.scrapeAndBuild()
    
    @updateProblemset.before_loop
    async def before_updateProblemset(self):
        await self.client.wait_until_ready()
    
async def setup(client: commands.Bot) -> None: 
    await client.add_cog(looper(client))