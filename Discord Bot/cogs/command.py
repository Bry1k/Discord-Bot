import discord  
from discord.ext import commands
from discord import app_commands
import aiohttp

class CommandCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_ready(self):
        print("Commands Ready")
        
    @app_commands.command(name="meme", description="Generates a random meme")
    async def meme(self, interaction: discord.Interaction):
        async with aiohttp.ClientSession() as session:
            async with session.get("https://meme-api.com/gimme/wholesomememes") as response:
                if response.status != 200:
                    await interaction.response.send_message("Could not fetch meme, try again later.", ephemeral=True)
                    return
                
                data = await response.json()
                embed = discord.Embed(title=data["title"], color=discord.Color.blue())
                embed.set_image(url=data["url"])
                await interaction.response.send_message(embed=embed)
                
    @app_commands.command(name="userinfo", description="Get information about a user")
    async def userinfo(self, interaction: discord.Interaction, user: discord.Member):
        embed = discord.Embed(title=f"User Info - {user}", color=discord.Color.blue())
        embed.add_field(name="Name", value=user.name, inline=True)
        embed.add_field(name="Bot", value=user.bot, inline=True)
        embed.add_field(name="Joined Server", value=user.joined_at.strftime("%Y-%m-%d"), inline=True)
        embed.add_field(name="Created Account", value=user.created_at.strftime("%Y-%m-%d"), inline=True)
        embed.set_thumbnail(url=user.avatar.url)
        
        await interaction.response.send_message(embed=embed)
        
    @app_commands.command(name="pfp", description="Shows the profile picture of a user")
    async def pfp(self, interaction: discord.Interaction, user: discord.Member):
        embed = discord.Embed(title=f"{user}'s Profile Picture", color=discord.Color.blue())
        embed.set_image(url=user.avatar.url)
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(CommandCog(bot))