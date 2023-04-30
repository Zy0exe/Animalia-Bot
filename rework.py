# Discord stuff
import discord
from discord import Embed
from discord import Game
from discord.ext import commands
from discord.ext.commands import cooldown

# Steam Stuff
import steam
from steam import steamid

# SQL Stuff
import mysql.connector

## More needed stuff
import json
import random
import os
import datetime
import traceback
import shutil
import asyncio


# Connect to the database
db = mysql.connector.connect(
    host="localhost", user="root", password="", database="kruger_park"
)

# Create a new Discord bot
bot = commands.Bot(command_prefix="!", help_command=None, intents=discord.Intents.all())


async def load():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            await bot.load_extension(f'cogs.{filename[:-3]}')

async def main():
    await load()
    await bot.start("TOKENHERE")

asyncio.run(main())
