import time

import discord 
from discord import app_commands
from discord.ext import commands, tasks

from utils import problem_helper as probh
from utils import datetime_helper as timeh

from models.app import App

class Looper(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client 
        self.app: App = client.app
        
        self.mainloop.start()
        self.updateProblemset.start()
    
    # 50 seconds should always fall somewhere in the 1 minute mark
    # but minimizes the amount of checks we have to do
    @tasks.loop(seconds=50)
    async def mainloop(self) -> None:
        dow = int(time.strftime('%w'))  # 0 = sunday, 6 = saturday
        hour = int(time.strftime('%H'))
        minute = int(time.strftime('%M'))
        
        intervals = [0, 15, 30, 45]  # 0=0, 15=1, 30=2, 45=3. problem intervals are 15 minutes
        if minute not in intervals:
            interval = None
        else:
            interval = minute // 15
            print(f"Interval: {interval}")  # debug print
            
        print(dow, hour, minute)
        
        # use the alert manager
    
        # for problem alerts
        # needs dow, hour, interval
        
        # for contest alerts
        # needs interval of contest away length
        # we can assume that the contests are technically static times
        # thus these technically won't change
        # set the specific contest times, calculate the current time away
        # check if its a proper interval,
        # if it is, then gather the alerts
        
        # for static alerts
        # since these are static times, when they occur, just gather the alerts and send
        
        # channel = self.client.get_channel(channelID)
        pass

    # update the problemset every 48 hours
    @tasks.loop(hours=48)
    async def updateProblemset(self) -> None:
        probh.updateProblemSet() # scrape new problems
        self.app.problemService.initProblemSets() # reinitialize the problem service

    @updateProblemset.before_loop
    @mainloop.before_loop
    async def before_loop(self) -> None:
        await self.client.wait_until_ready()

async def setup(client: commands.Bot) -> None: 
    await client.add_cog(Looper(client))