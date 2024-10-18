"""
ADD THIS 
"""

import discord
from discord.ext import commands

class UserSettings(commands.Cog):
    def __init__(self, client):
        self.client = client

    # opt command
    # lets the user opt into / out of an event. works as a toggle. 
    # can opt into the problems or opt into the contests. 
    # output that signals the change should be ephemeral. 
    # will add / remove a role if roles are active. 
    # sends an error if server isn't setup. 
    
    
    # /uinfo command 