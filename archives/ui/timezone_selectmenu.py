import discord

from managers import server_settings_manager as ssm

from ui import embed_styler as ems 

# TODO: list all the timezones here
# When i use them in server_settings.py use a for loop to from importing this to read and itearte it
# same below, iterate over a simple list to build the selectOptions
timezones = [

]

class Timezone(discord.ui.View):
    def __init__(self):
        super().__init__(timeout = 30)
        self.add_item(TimezoneMenu())

class TimezoneMenu(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label = "UTC", value = "UTC"),
            discord.SelectOption(label = "UTC-1", value = "UTC-1"),
            discord.SelectOption(label = "UTC-2", value = "UTC-3"),
        ]
        super().__init__(
            placeholder="Testing", 
            options = options, 
            min_values = 1, 
            max_values = 1,
        )

    async def callback(self, interaction: discord.Interaction):

        timezone = self.values[0]

        if ssm.updateServer(interaction.guild.id, "timezone", timezone):
            await interaction.response.send_message(embed = ems.styleSimpleEmbed("Success!", "You have successfully set the timezone.", discord.Color.green()), ephemeral = True)
        else:
            await interaction.response.send_message(embed = ems.styleSimpleEmbed("Failure", "Perhaps you're not setup? \nTry `/serversetup`", discord.Color.red()), ephemeral = True)
    