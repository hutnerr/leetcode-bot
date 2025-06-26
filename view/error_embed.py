import discord.embeds

class ErrorEmbed(discord.Embed):
    def __init__(self, code: str, msg:str, help:str):
        super().__init__(title=f"ERROR `{code}`", description="First try `/help <command>`.\nIf you believe this is an issue please submit on [GitHub](https://github.com/hutnerr/leetcode-bot/issues) using `/report`.")
        
        self.add_field(name="Message", value=str(msg), inline=False)
        self.add_field(name="Help", value=help if help else "This is likely a backend issue, please try again later.", inline=False)

        self.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/3/34/ErrorMessage.png")
        self.color = discord.Color.red()
