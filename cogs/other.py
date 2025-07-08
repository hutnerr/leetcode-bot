import discord
from discord import app_commands
from discord.ext import commands

from models.app import App
from errors.simple_exception import SimpleException

from view.error_embed import ErrorEmbed
from view.help_embed import HelpEmbed, CommandHelpEmbed

helpDictionary = {
    "problem": {
        "description": "Gets a LeetCode problem using certain parameters.\n\nThe parameters are difficulty and premium.\nPremium is optional. It is free by default.\n\nDifficulty can be easy, medium, hard, or random.\nPremium can be free, paid, or all.\n",
        "usage": "/problem <difficulty> <premium>",
    },
    "dailyproblem": {
        "description": "Gets the LeetCode daily problem.",
        "usage": "/dailyproblem",
    },
    "help": {
        "description": "Displays help information specific commands within the bot.",
        "usage": "/help <command>",
    },
    "report": {
        "description": "Provides a link which allows users to report an issue to the GitHub.",
        "usage": "/report",
    },
    "about": {
        "description": "Displays information about the bot.",
        "usage": "/about",
    },
    "uinfo": {
        "description": "Gets information about a user, such as their LeetCode username and problem completion stats.\n\nIf no user is specified, it will use whoever called the command.",
        "usage": "/uinfo <user>",
    },
    "deluser": {
        "description": "Deletes your user data from the bot.\n\nThis will remove your LeetCode username and any other data associated with your user. It is NOT server specific, it will delete your data entirely.\n\nThis is useful if you want to reset your data or if you no longer want to use the bot.",
        "usage": "/deluser",
    },
    "setusername": {
        "description": "Sets your LeetCode username for the bot to use.",
        "usage": "/setusername <username>",
    },
    "leaderboard": {
        "description": "Displays the leaderboard for a specific server.\n\nThis will show the top users in the server based on their points.",
        "usage": "/leaderboard",
    },
    "rank": {
        "description": "Gets a users rank in the server based on your points.\n\nThis will show your rank and how many points you have.\n\nBy default it will use the user who called the command, but you can specify another user.",
        "usage": "/rank <user>",
    },
}


class OtherCog(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client: commands.Bot = client
        self.app: App = client.app

    # help command to display help information for the bot
    # uses a dictionary to store the help information for each command
    # TODO: if no parameter give information and how to use the bot
    @app_commands.command(name='help', description='Displays help information for the bot')
    @app_commands.choices(command=[app_commands.Choice(name=cmd, value=cmd) for cmd in helpDictionary.keys()])
    async def help(self, interaction: discord.Interaction, command: app_commands.Choice[str] = None):
        if command is None:
            # if no command is specified, send a general help message
            await interaction.response.send_message(embed=HelpEmbed(), ephemeral=True)
            return
        
        command = command.value
        info = helpDictionary.get(command)
        if info:
            await interaction.response.send_message(embed=CommandHelpEmbed(command, info), ephemeral=True)
        else:
            raise SimpleException("HELP", f"{command} was not found")

    # report command to provide a link to report issues
    # this is a simple command that just sends a message with a link to the GitHub
    @app_commands.command(name='report', description='Report an issue to the GitHub')
    async def report(self, interaction: discord.Interaction):
        await interaction.response.send_message("Please report issues **[here](https://github.com/hutnerr/leetcode-bot/issues)**.", ephemeral=True)

    # about command to display information about the bot
    @app_commands.command(name='about', description='Displays information about the bot')
    async def about(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="About",
            description="This bot was created to help facilitate the use of [LeetCode](https://leetcode.com/) on Discord.\n\n"
            "It provides commands to interact with LeetCode problems and contests easily, however, its main purpose is to provide a system of reoccurring problems to a specific server.\n\n"
            "The bot is [open source](https://github.com/hutnerr/leetcode-bot) and contributions are welcome.",
            color=discord.Color.green()
        )
        embed.add_field(
            name="Developer", value="> [My GitHub](https://github.com/hutnerr)\n> [My Website](https://hunter-baker.com)", inline=False)
        embed.add_field(
            name="GitHub", value="> [LeetCode Bot](https://github.com/hutnerr/leetcode-bot)", inline=False)
        await interaction.response.send_message(embed=embed)

    @help.error
    @report.error
    @about.error
    async def errorHandler(self, interaction: discord.Interaction, error: app_commands.CommandInvokeError):
        exception: SimpleException = error.original
        code: SimpleException = exception.code if isinstance(error.original, SimpleException) else "BACKEND FAILURE"
        msg = error.original.message if isinstance(error.original, SimpleException) else str(error.original)
        help = error.original.help if isinstance(error.original, SimpleException) else None
        await interaction.response.send_message(embed=ErrorEmbed(code, msg, help), ephemeral=True)


async def setup(client: commands.Bot) -> None:
    await client.add_cog(OtherCog(client))
