import discord  
from discord.ext import commands
from discord import app_commands

class Mod(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_ready(self):
        print("Moderation commands ready")
        
    def is_admin():
        async def predicate(interaction: discord.Interaction) -> bool:
            return interaction.user.guild_permissions.administrator
        return app_commands.check(predicate)

    @app_commands.command(name="clear", description="Delete specified amount of messages from channel")
    @app_commands.default_permissions(administrator=True)
    @is_admin()
    async def delete_messages(self, interaction: discord.Interaction, amount: int):
        if amount < 1:
            await interaction.channel.send("Please specify a value greater than 1")
            return
        await interaction.response.send_message(f"{amount} messages are being deleted", ephemeral=True)
        deleted_messages = await interaction.channel.purge(limit=amount)
        await interaction.channel.send(f"Deleted {len(deleted_messages)} messages")
        
    @app_commands.command(name="kick", description="Kick a user from the server")
    @app_commands.default_permissions(administrator=True)
    @is_admin()
    async def kick(self, interaction: discord.Interaction, user: discord.Member):
        await user.kick()
        await interaction.response.send_message(f"{user} has been kicked", ephemeral=True)
        
    @app_commands.command(name="ban", description="Ban a user from the server")
    @app_commands.default_permissions(administrator=True)
    @is_admin()
    async def ban(self, interaction: discord.Interaction, user: discord.Member):
        await interaction.guild.ban(user)
        await interaction.response.send_message(f"{user} has been banned", ephemeral=True)
        
    @app_commands.command(name="unban", description="Unban a user by user id")
    @app_commands.default_permissions(administrator=True)
    @is_admin()
    async def unban(self, interaction: discord.Interaction, user_id: str):
        user = await self.bot.fetch_user(user_id)
        await interaction.guild.unban(user)
        await interaction.response.send_message(f"{user} has been unbanned", ephemeral=True)
        
async def setup(bot):
    await bot.add_cog(Mod(bot))