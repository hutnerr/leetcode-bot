import discord
from discord import app_commands
from discord.ext import commands

from models.app import App
from errors.simple_exception import SimpleException

from view.error_embed import ErrorEmbed
from view.positive_embed import PositiveEmbed
from view.help_embed import HelpEmbed, CommandHelpEmbed

helpDictionary = {
    "about": {
        "description": "Displays information about the bot and it's purpose.",
        "usage": "/about",
    },
    "contests": {
        "description": "Gets information about the current LeetCode contests. It will show the upcoming contests this week, how far away they are, and provide a link to register.",
        "usage": "/contests",
    },
    "dailylcproblem": {
        "description": "Gets the official LeetCode daily problem.",
        "usage": "/dailylcproblem",
    },
    "deleteproblem": {
        "description": "Deletes a problem configuration from the problems list.\n\nThis will remove the problem configuration from the server's reoccurring problems and it will no longer be sent.",
        "usage": "/deleteproblem <problemID>",
    },
    "deleteserver": {
        "description": "Deletes the server configuration.\n\nThis will remove the server's reoccurring problems and any other server specific data. It will delete the server's data entirely.",
        "usage": "/deleteserver",
    },
    "deleteuser": {
        "description": "Deletes your user data from the bot.\n\nThis will remove your LeetCode username and any other data associated with your user. It is NOT server specific, it will delete your data entirely.\n\nThis is useful if you want to reset your data or if you no longer want to use the bot.",
        "usage": "/deleteuser",
    },
    "help": {
        "description": "Displays help information about the bot. Supports general help information as well as specific commands within the bot.",
        "usage": "/help or /help <command>",
    },
    "leaderboard": {
        "description": "Displays the leaderboard for a specific server.\n\nThis will show the top users in the server based on their points.",
        "usage": "/leaderboard",
    },
    "problemactive" : {
        "description": "Gets the active problems in the server.\n\nThis will show the problems that can be submitted for points through `/submit`. For a problem to count, it might be one of your recent 15 submissions.",
        "usage": "/problemactive",
    },
    "problemconfig": {
        "description": "Configures the server's reoccurring problems.\n\nThis will allow you to add and configure the server's reoccurring problems. It is used to set up the problems that will be sent to the server on a schedule.",
        "usage": "/problemconfig <problemID>",
    },
    "probleminfo": {
        "description": "Displays information about the configured problems in the server.\n\nThis will show the problems that are configured in the server and their details.",
        "usage": "/probleminfo",
    },
    "lcproblem": {
        "description": "Gets a LeetCode problem using certain parameters.\n\nThe parameters are difficulty and premium.\nPremium is optional. It is free by default.\n\nDifficulty can be easy, medium, hard, or random.\nPremium can be free, paid, or all.\n",
        "usage": "/lcproblem <difficulty> <premium>",
    },
    "rank": {
        "description": "Gets a users rank in the server based on your points.\n\nThis will show your rank and how many points you have.\n\nBy default it will use the user who called the command, but you can specify another user.",
        "usage": "/rank <user>",
    },
    "report": {
        "description": "Provides a link which allows users to report an issue to the GitHub.",
        "usage": "/report",
    },
    "resetdupes": {
        "description": "Resets the duplicate problems in the server.\n\nThis will remove any duplicate problems in the server's reoccurring problems.",
        "usage": "/resetdupes",
    },
    "serverconfig": {
        "description": "Configures the server's settings.\n\nTo learn more about the server settings use just `/help`.",
        "usage": "/serverconfig <setting group>",
    },
    "setusername": {
        "description": "Sets your LeetCode username for the bot to use.",
        "usage": "/setusername <username>",
    },
    "serverinfo": {
        "description": "Displays the  server's configuration.",
        "usage": "/serverinfo",
    },
    "submitproblems": {
        "description": "Submits your recent LeetCode submissions to the server for points.\n\nThis will check your recent 15 submissions and give you points for any active problems (`/problemactive`) that you have completed.",
        "usage": "/submitproblems",
    },
    "userinfo": {
        "description": "Gets information about a user, such as their LeetCode username and problem completion stats.\n\nIf no user is specified, it will use whoever called the command.",
        "usage": "/userinfo <user>",
    },
    "vote": {
        "description": "Show support for the bot by voting for it on Top.gg",
        "usage": "/vote",
    },
    "tutorial": {
        "description": "Provides a link to the bot's setup tutorial.",
        "usage": "/tutorial",
    }
}


class OtherCog(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client: commands.Bot = client
        self.app: App = client.app

    # help command to display help information for the bot
    # uses a dictionary to store the help information for each command
    @app_commands.command(name='help', description='Displays help information for the bot')
    @app_commands.choices(command=[app_commands.Choice(name=cmd, value=cmd) for cmd in helpDictionary.keys()])
    async def help(self, interaction: discord.Interaction, command: app_commands.Choice[str] = None):
        if command is None:
            # if no command is specified, send a general help message
            await interaction.response.send_message(embed=HelpEmbed())
            return
        
        command = command.value
        info = helpDictionary.get(command)
        if info:
            await interaction.response.send_message(embed=CommandHelpEmbed(command, info))
        else:
            raise SimpleException("HELP", f"{command} was not found")

    # report command to provide a link to report issues
    # this is a simple command that just sends a message with a link to the GitHub
    @app_commands.command(name='report', description='Report an issue to the GitHub')
    async def report(self, interaction: discord.Interaction):
        embed = PositiveEmbed(
            title="Report an Issue",
            description="If you encounter any issues with the bot, please report them on the [GitHub repository](https://github.com/hutnerr/leetcode-bot/issues).",
            thumbnail="https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png",
            url="https://github.com/hutnerr/leetcode-bot/issues"
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)

    # about command to display information about the bot
    @app_commands.command(name='about', description='Displays information about the bot & it\'s purpose')
    async def about(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="About",
            description="This bot was created to help facilitate the use of [LeetCode](https://leetcode.com/) on Discord.\n\n"
            "It provides commands to interact with LeetCode problems and contests easily, however, its main purpose is to provide a system of reoccurring problems to a specific server.\n\n"
            "The bot is [open source](https://github.com/hutnerr/leetcode-bot) and contributions are welcome.",
            color=discord.Color.green()
        )
        embed.add_field(name="Developer", value="> [My GitHub](https://github.com/hutnerr)\n> [My Website](https://hunter-baker.com)", inline=False)
        embed.add_field(name="GitHub", value="> [LeetCode Bot](https://github.com/hutnerr/leetcode-bot)", inline=False)
        await interaction.response.send_message(embed=embed)


    @app_commands.command(name="tutorial", description="Provides a link to the bot's setup tutorial")
    async def tutorial(self, interaction: discord.Interaction):
        url = "https://www.hunter-baker.com/beastcode-help.html"
        embed = PositiveEmbed(
            title="Tutorial",
            description=f"To learn how to set up the bot, please visit the [setup tutorial]({url}). At the top of the page is some additional information. Near the bottom is a walkthrough of the setup process.",
        )
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="vote", description="Show support for the bot by voting for it on Top.gg")
    async def vote(self, interaction: discord.Interaction):
        url = "https://top.gg/bot/1392738606120173719"
        embed = PositiveEmbed(
            title="Vote",
            description=f"To vote for the bot, please visit the [vote page]({url}). Any feedback is much appreciated! I am a new developer and I am always looking to improve the bot. Thank you very much.",
        )
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
