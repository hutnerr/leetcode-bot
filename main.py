############################################################################################################################## IMPORTS 
import platform
import time
from typing import Literal
import json

import discord
from colorama import Back, Fore, Style
from discord import app_commands
from discord.ext import commands

############################################################################################################################## CLIENT SETUP

class Client(commands.Bot):
    
    # Constructor that sets up the base client. 
    def __init__(self):
        intents = discord.Intents().all()
        super().__init__(command_prefix = commands.when_mentioned_or("/"), intents = intents)
        
        self.cogslist = [
            "cogs.problems",
            "cogs.SelectMenuTest",
            "cogs.Loooooping"
        ]

    # Loads cogs
    async def setup_hook(self) -> None:
        for ext in self.cogslist:
            await self.load_extension(ext)

    # Prints out system info, syncs slash commands to the tree, and changes the bots status
    async def on_ready(self):
        prfx = (Back.BLACK + Fore.GREEN + time.strftime("%H:%M:%S EST", time.localtime()) + Back.RESET + Fore.WHITE + Style.BRIGHT)
        print(prfx + " Logged in as " + Fore.YELLOW + client.user.name)
        print(prfx + " Bot ID " + Fore.YELLOW + str(client.user.id))
        print(prfx + " Discord Version " + Fore.YELLOW + discord.__version__) 
        print(prfx + " Python Version " + Fore.YELLOW + str(platform.python_version()))
        synced = await client.tree.sync()
        print(prfx + " Slash CMDs Sycned " + Fore.YELLOW + str(len(synced)))
        await client.change_presence(activity = discord.Activity(type = discord.ActivityType.playing, name = "/help for commands"))

# Create our main client ( Bot ) object   
client = Client()
client.remove_command("help") # remove default help so I can add custom one. 

############################################################################################################################## Run the Bot

with open("data/data.json", "r") as file:
    temp = json.load(file)['key']

client.run(temp)
