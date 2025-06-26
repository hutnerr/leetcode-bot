import discord
from errors.simple_exception import SimpleException
from models.server import Server
from view.error_embed import ErrorEmbed

class ChannelSelectorView(discord.ui.View):
    def __init__(self, server: Server):
        super().__init__()
        self.add_item(ChannelSelector(server))

class ChannelSelector(discord.ui.ChannelSelect):
    def __init__(self, server: Server):
        super().__init__()
        self.server = server
        self.min_values = 1
        self.max_values = 1

    async def callback(self, interaction: discord.Interaction):
        if self.values is None or len(self.values) == 0:
            raise SimpleException("INVALID SELECTION")
        
        channel = self.values[0]
        if channel.type != discord.ChannelType.text:
            # FIXME: this exception isn't being caught by the error handler
            # it should be caught and handled gracefully, but currently it raises an unhandled exception
            code = "CHNSELVW"
            msg = "The selected channel is not a text channel."
            help = "If your channel is not listed, try doing `/setchannel #channel_name` to set it as the output channel directly."
            await interaction.response.send_message(embed=ErrorEmbed(code, msg, help), ephemeral=True)
            return
            
        # update the server settings with the selected channel
        channel = self.values[0]
        self.server.settings.postingChannelID = int(channel.id)
        self.server.toJSON()
        await interaction.response.send_message(f"Server Channel set to: <#{channel.id}>", ephemeral=True)