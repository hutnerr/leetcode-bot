import discord
from discord import app_commands
from discord.ext import commands, tasks
import asyncio

from datetime import datetime, timezone

import modules.ProblemsHandler as pt
import modules.SettingHandler as sh

######################################################################

def makeTimes():
    options = []

    options.append(discord.SelectOption(label = "12:00 (12:00 A.M.)", value = "00:00"))

    for i in range(1, 24):
        options.append(discord.SelectOption(label = f"{i}:00 ({i % 12 if i != 12 else 12}:00 {'A.M.' if i <= 12 else 'P.M.'})", value = f"{i}:00"))
    return options

class TimeMenu(discord.ui.Select):
    def __init__(self):
        super().__init__(placeholder="What hour?", options = makeTimes(), min_values = 1, max_values = 1)

    async def callback(self, interaction: discord.Interaction):
        values = ", ".join(self.values)
        sh.updateServerFile(interaction.guild_id, "dailies", "hour", values)
        await interaction.response.send_message(content=f"Time changed to: **{values}** ")

class TimeZoneMenu(discord.ui.Select):
    def __init__(self):
        super().__init__(placeholder="What timezone?", options = [
            discord.SelectOption(label = "EST", value = "EST"),
            discord.SelectOption(label = "CST", value = "CST"),
            discord.SelectOption(label = "PST", value = "PST"),
            discord.SelectOption(label = "UTC", value = "UTC"),
            discord.SelectOption(label = "IST", value = "IST"),
            discord.SelectOption(label = "AEST", value = "AEST"),
            discord.SelectOption(label = "NZST", value = "NZST")
        ], min_values = 1, max_values = 1)

    async def callback(self, interaction: discord.Interaction):
        values = ", ".join(self.values)

        sh.updateServerFile(interaction.guild_id, "dailies", "timezone", values)
        await interaction.response.send_message(content=f"Timezone changed to: **{values}** ")

class ToggleCustomDailies(discord.ui.Select):
    def __init__(self):
        super().__init__(placeholder="Custom Dailies On?", options = [
            discord.SelectOption(label = "Yes", value = "true"),
            discord.SelectOption(label = "No", value = "false")
        ], min_values = 1, max_values = 1)

    async def callback(self, interaction: discord.Interaction):
        values = ", ".join(self.values)
        sh.updateServerFile(interaction.guild_id, "dailies", "active", values)
        await interaction.response.send_message(content=f"Custom Dailies toggled to: **{values}** ")

class ToggleWeeklyContests(discord.ui.Select):
    def __init__(self):
        super().__init__(placeholder="Weekly Contest Alerts On?", options = [
            discord.SelectOption(label = "Yes", value = "true"),
            discord.SelectOption(label = "No", value = "false")
        ], min_values = 1, max_values = 1)

    async def callback(self, interaction: discord.Interaction):
        values = ", ".join(self.values)
        sh.updateServerFile(interaction.guild_id, "contests", "weekly", values)
        await interaction.response.send_message(content=f"Weekly Contests toggled to: **{values}** ")

class ToggleBiweeklyContests(discord.ui.Select):
    def __init__(self):
        super().__init__(placeholder="Biweekly Contests Alerts On?", options = [
            discord.SelectOption(label = "Yes", value = "true"),
            discord.SelectOption(label = "No", value = "false")
        ], min_values = 1, max_values = 1)

    async def callback(self, interaction: discord.Interaction):
        values = ", ".join(self.values)
        sh.updateServerFile(interaction.guild_id, "contests", "biweekly", values)
        await interaction.response.send_message(content=f"Weekly Contests toggled to: **{values}** ")

class Select(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(ToggleCustomDailies())
        self.add_item(TimeMenu())
        self.add_item(TimeZoneMenu())
        self.add_item(ToggleWeeklyContests())
        self.add_item(ToggleBiweeklyContests())

class SelectMenuTest(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @app_commands.command(name = 'test', description='Test command')
    async def test(self, interaction: discord.Interaction):
        await interaction.response.send_message(content = "# Settings", view = Select())
        # await asyncio.sleep(1)
        # await interaction.response.send_message(content = interaction.user.mention, ephemeral = True)

######################################################################

async def setup(client: commands.Bot) -> None: 
    await client.add_cog(SelectMenuTest(client))
