import discord

class CommandHelpEmbed(discord.Embed):
    def __init__(self, command: str, info: dict):
        super().__init__(
            title=f"Help for `{command}`", description=info['description'])
        self.add_field(name="Usage", value=f"`{info['usage']}`", inline=False)
        self.color = discord.Color.blue()
        self.set_footer(text="Use /help to see general help.")

class HelpEmbed(discord.Embed):
    def __init__(self):
        super().__init__(title="General Help",
                         description="This bot provides commands to interact with LeetCode problems and contests easily. To view all commands, use `/help <command>` and browse through the available commands. Below is a brief overview of some information that might not be immediately obvious.")
        
        self.add_field(name="Server Configuration", 
                       value="Use `/serverconfig` to configure the server settings for LeetCode problems and contests. These commands are for Server Admins only. \n"
                       "- `Upcoming Contest Alerts`: If on, a notification will be sent out on the chosen intervals about an upcoming contest. For example, on a 30min interval, a notification will appear when a contest is 30mins away.\n"
                       "- `Static Time Alerts`: If these are turned on, whenever the time comes for this event, a notification will be sent. For example, if Official Daily Alerts are on, a notification will be sent every day when the daily problem is refreshed.\n"
                       "- `Other Settings`: These are a collection of other relevant settings. Timezone ensures that the bot operates on the right time. Duplicates allowed, if on, will prevent problems that have already been sent from appearing again. Alert Role is the role that the bot should @mention on notifications. Use Alert Role toggles this on/off. Bot Channel is the channel the bot should output notifications to.", inline=False)
        
        self.add_field(name="Problem Configuration",
                       value="One of the main features that this bot supplies is providing reoccuring problems based on specified settings. Use `/problemconfig <problemID>` to configure the server's problem settings. The problem ID is simply an identifier to differentiate the problems and their unique settings. If a problem exists, then it will be sent. To remove a problem use `/deleteproblem`. These commands are for Server Admins only. \n\n"
                       "The problem will be sent at the configured time on the specified days of the week. You can change settings such as the difficulty and if premium problems should be included. If there is more than one difficulty, it will be a random selection.", inline=False)
        
        self.add_field(name="User Commands",
                       value="For users to be part of the submissions system, they must first use `/setusername` to link their profile. "
                       "If a user wishes to delete their profile, they can use `/deleteuser`.", inline=False)

        self.color = discord.Color.blue()
        self.set_footer(
            text="Use /help <command> to see command specific help.")
