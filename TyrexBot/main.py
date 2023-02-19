import discord
from discord.ext import commands
import os
from discord import *
import logging
import json
import asyncio
import json

#for log everything from our bot when we faced an error
logHandler = logging.basicConfig(filename='discord.log' , filemode='w')

#getting our bot token from "config.json"
_TOKEN = json.load(open('config.json' , 'r'))

#create bot object from commands.Bot
bot = commands.Bot(command_prefix='*' , intents=discord.Intents.all() , case_insensitive=False , help_command=None)


#for changing our status bot and print log when we coming online
@bot.event
async def on_ready():

    await bot.change_presence(status = discord.Status.idle , activity = discord.Activity(type=discord.ActivityType.watching , name=f"{len(bot.users)} users | *help"))
    print(f"we logged as id : {bot.user.id} name : {bot.user.name}")




####################
#load all cogs and running bot 
async def load():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            await bot.load_extension(f'cogs.{filename[:-3]}')

 
async def main():
    await load()
    await bot.start(token=_TOKEN)

asyncio.run(main())
####################
