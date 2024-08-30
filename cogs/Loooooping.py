import csv
import os
import random
from datetime import datetime, time
from typing import Any

import asyncio

import discord
from discord import app_commands
from discord.ext import commands, tasks

from modulesSmile import Loopers
from modulesSmile import ProblemsHandler as ph

class Loooooping(commands.Cog):

    def __init__(self, client: commands.Bot) -> None:
        self.client = client
        self.dailyLeetcode.start()

    @tasks.loop(seconds = 10) # Check every 10 seconds
    async def dailyLeetcode(self) -> None:

        # now = datetime.now()
        # minutes = now.minute

        # print(minutes)

        # if minutes != 0:
        #     return
        
        # file = open("data/times/{minutes}.txt", "r")

        print("START")

        servers = None

        with open(f"data/times/{2}.txt", "r") as file:
            servers = file.readlines()
            for server in servers:
                server = server.strip()
                info = Loopers.applyDaily(server)
                channel = self.client.get_channel(info[1]) 
                await channel.send(embed = ph.prettifyProblem(info[2]))

        print("END")

    @dailyLeetcode.before_loop
    async def before_say_hello(self) -> None:
        await self.client.wait_until_ready()

async def setup(client: commands.Bot) -> None: 
    await client.add_cog(Loooooping(client))




