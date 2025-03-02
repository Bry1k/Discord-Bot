import discord
from discord.ext import commands

import os
import asyncio
from itertools import cycle
import logging
from dotenv import load_dotenv

load_dotenv("./dotenv/.env")
TOKEN: str =  os.getenv("TOKEN")

bot = commands.Bot(command_prefix=".", intents=discord.Intents.all())

@bot.event
async def on_ready():
    print("Bot is ready")   
    try:
        synced_commands = await bot.tree.sync()
        print(f"Synced {len(synced_commands)} commands") 
    except Exception as e:
        print("Error with syncing application commands has occured: ", e)
        

@bot.tree.command(name ="hello", description="Says hello to the user")
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message(f"{interaction.user.mention} Hello!")

    
async def Load():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}") 

async def main():
    async with bot:
        await Load()
        await bot.start(TOKEN)
    
   
asyncio.run(main())