"""
This is the main file for the bot. It will handle the setup of the bot, and the loading of the cogs.
This is where the bot will be run from.
"""
import time
import json

import discord
from colorama import Back, Fore, Style
from discord.ext import commands

from utils.initializer import Initializer
from models.app import App

class Client(commands.Bot):
    def __init__(self):
        intents = discord.Intents().all()
        super().__init__(command_prefix = commands.when_mentioned_or("/"), intents = intents)
        
        self.app: App = None # the app instance will be set in on_ready, it is the main backend 
        self.cogslist = [
            "cogs.problems",
            "cogs.other",
            "cogs.contests",
            "cogs.user",
            # "cogs.submitter", # TODO: Add this back when I finish the working version 
            # "cogs.looper",
            # "cogs.user_settings",
            # "cogs.server_settings",
        ]

    async def setup_hook(self) -> None:
        # the "app" is the main backend & data container for the bot
        # it contains all the servers, users, buckets, services, and mediators, etc.
        self.app = Initializer.initApp()
        
        for ext in self.cogslist:
            await self.load_extension(ext) # loads our cogs    

    # prints info to console, gives us custom status, and syncs slash commands
    async def on_ready(self):
        prfx = (Back.BLACK + Fore.GREEN + time.strftime("%H:%M:%S EST", time.localtime()) + Back.RESET + Fore.WHITE + Style.BRIGHT)
        print(prfx + " Logged in as " + Fore.YELLOW + client.user.name)
        synced = await client.tree.sync()
        print(prfx + " Slash CMDs Sycned " + Fore.YELLOW + str(len(synced)))
        await client.change_presence(activity = discord.Activity(type = discord.ActivityType.playing, name = "/help for commands"))

client = Client()
client.remove_command("help") # remove default help so I can add custom one. 

with open("data/key.json", "r") as file:
    key = json.load(file)['key']

client.run(key)