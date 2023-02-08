import discord
from discord.ext import commands
import asyncio
import time
import discord.ext.commands
from discord.ext.commands import MissingPermissions



#this command use for clear messages 
class Clear(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.command(name='clear' , aliases = ['clr'])
    @commands.has_permissions(manage_messages = True)
    async def clear(self,msg , limit = 100):    
            await msg.reply(f"`{limit} Messages :` will be deleted in 5 Sec.. <a:loading:1067888489946955776>" , delete_after = 5)
            time.sleep(5)
            await msg.channel.purge(limit = limit)
    
    @clear.error
    async def clear_error(self, msg , error):
        if isinstance(error , MissingPermissions):
                await msg.send("**you dont have permission! [permission require is manage message]**")
       
 
async def setup(bot):
    await bot.add_cog(Clear(bot))