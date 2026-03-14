"""
This is the main file for the bot. It will handle the setup of the bot, and the loading of the cogs.
This is where the bot will be run from.
"""
import time
import json
import os

import discord
from colorama import Back, Fore, Style
from discord.ext import commands

from utils.initializer import Initializer
from models.app import App

from pyutils import get_env
from pyutils import Clogger, CloggerColor, LogLevel, CloggerConfig, Clogobj, ClogobjFactory

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
            "cogs.looper",
            "cogs.competition",
            "cogs.server",
        ]

    async def setup_hook(self) -> None:
        # the "app" is the main backend & data container for the bot
        # it contains all the servers, users, buckets, services, and mediators, etc.
        self.app = Initializer.initApp()
        
        for ext in self.cogslist:
            await self.load_extension(ext) # loads our cogs   
             
        Clogger.info(f"App initialized with {len(self.app.servers)} servers, {len(self.app.users)} users.")
        

    # prints info to console, gives us custom status, and syncs slash commands
    async def on_ready(self):        
        prfx = (Back.BLACK + Fore.GREEN + time.strftime("%H:%M:%S EST", time.localtime()) + Back.RESET + Fore.WHITE + Style.BRIGHT)
        Clogger.info("Logged in as " + Fore.YELLOW + client.user.name)
        synced = await client.tree.sync()
        Clogger.info("Slash CMDs Sycned " + Fore.YELLOW + str(len(synced)))
        await client.change_presence(activity = discord.Activity(type = discord.ActivityType.playing, name = "/help for commands"))
        Clogger.info("Bot is ready!")

    async def sendErrAlert(self, message: str):
        Clogger.info("Sending error alert to user...")
        userID = get_env("ALERT_DISCORD_ID")
        if not userID:
            Clogger.warn("ALERT_DISCORD_ID not set in environment variables. Cannot send error alert.")
            return
        
        user = await self.fetch_user(int(userID))
        if not user:
            Clogger.warn(f"User with ID {userID} not found. Cannot send error alert.")
            return
        
        await user.send(message)

if __name__ == "__main__":
    client = Client()
    client.remove_command("help") # remove default help so I can add custom one. 

    # base config
    Clogger.config = CloggerConfig(
        write_to_file=True,
        log_file_path=os.path.join("logs", "bot.log")
    )

    ENV_NAME = "BEASTCODE_BOT_TOKEN"
    # ENV_NAME = "TESTING_BOT_TOKEN"
    key = get_env(ENV_NAME)
    if not key:
        Clogger.error(
            f"Bot token not found in environment variable '{ENV_NAME}'. Please set it and try again.", 
            exc=Exception
        )

    Clogger.info("Starting bot...")
    client.run(key)