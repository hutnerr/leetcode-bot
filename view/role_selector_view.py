import discord
from errors.simple_exception import SimpleException
from models.server import Server

class RoleSelectorView(discord.ui.View):
    def __init__(self, server: Server):
        super().__init__()
        self.add_item(RoleSelector(server))

class RoleSelector(discord.ui.RoleSelect):
    def __init__(self, server: Server):
        super().__init__()
        self.server = server
        self.min_values = 1
        self.max_values = 1

    async def callback(self, interaction: discord.Interaction):
        if self.values is None or len(self.values) == 0:
            raise SimpleException("ROLES", "Invalid role selection.", "Please select a valid role from the dropdown menu.")
        
        # update the server settings with the selected role
        role = self.values[0]
        self.server.settings.alertRoleID = int(role.id)
        self.server.toJSON()
        await interaction.response.send_message(f"Server Role set to: <@&{role.id}>", ephemeral=True)