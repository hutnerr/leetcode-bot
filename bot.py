import time
import json

import discord
from colorama import Back, Fore, Style
from discord.ext import commands

# --------------------------------- # 
# Client Class & Setup
# --------------------------------- #

class Client(commands.Bot):
    def __init__(self):
        intents = discord.Intents().all()
        super().__init__(command_prefix = commands.when_mentioned_or("/"), intents = intents)
        
        self.cogslist = [
            "cogs.problems",
            "cogs.submitter",
            "cogs.looper",
            "cogs.contests",
        ]

    async def setup_hook(self) -> None:
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

with open("key.json", "r") as file:
    temp = json.load(file)['key']

client.run(temp)