import discord.embeds

class ConfirmationEmbed(discord.Embed):
    def __init__(self, msg:str):
        super().__init__(title="Are you sure?", description=msg)
        
        self.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/f/f6/Lol_question_mark.png")
        self.color = discord.Color.yellow()

class ConfirmationView(discord.ui.View):
    def __init__(self, timeout = 15):
        super().__init__(timeout=timeout)
        self.result = None  # default is None, user did not confirm action

    @discord.ui.button(label = "Yes", style = discord.ButtonStyle.green)
    async def accept(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.result = True
        await interaction.response.defer()
        self.stop()

    @discord.ui.button(label = "No", style = discord.ButtonStyle.red)
    async def reject(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.result = False
        await interaction.response.defer()
        self.stop()