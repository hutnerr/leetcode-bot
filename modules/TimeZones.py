from datetime import datetime, timezone

# Get the current datetime
current_datetime = datetime.now()

# Convert the datetime to UTC
utc_datetime = current_datetime.astimezone(timezone.utc)

print("Current datetime:", current_datetime)
print("UTC datetime:", utc_datetime)

def timeConvert(dt):
    utc_datetime = dt.astimezone(timezone.utc)

    # @app_commands.command(name = 'test', description='Test command')
    # async def test(self, interaction: discord.Interaction):
    #     x = interaction.created_at.astimezone(timezone.utc)
    #     await interaction.response.send_message(x)