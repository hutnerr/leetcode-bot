import discord

class PositiveEmbed(discord.Embed):
    def __init__(self, title: str, description: str = None, url: str = None, thumbnail: discord.Asset = None):
        super().__init__(title=title, description=description, url=url, color=discord.Color.green())
        
        if thumbnail:
            self.set_thumbnail(url=thumbnail)
        else:
            self.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/5/56/Check_icon.png")