import discord
from discord import File
from discord.ext import commands
import json
import logging
import asyncio
from async_timeout import timeout
import os


#getting log file 
handler = logging.basicConfig(filename='discord.log' , filemode='w')



#get token from json file 
TOKEN = json.load(open('config.json' , 'r'))



#create bot object from commands.Bot
bot = commands.Bot(command_prefix='=' , intents=discord.Intents.all() , case_insensitive=False , help_command=None)


#console log and changing presence 
@bot.event
async def on_ready():
        await bot.change_presence(status = discord.Status.online , activity = discord.Activity(type=discord.ActivityType.watching , name=f"{len(bot.users)} users"))
        print(f"logged in {bot.user.name}")





####################
#load all cogs and running bot 
async def load():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            await bot.load_extension(f'cogs.{filename[:-3]}')

 
async def main():
    await load()
    await bot.start(token=TOKEN)

asyncio.run(main())
####################
