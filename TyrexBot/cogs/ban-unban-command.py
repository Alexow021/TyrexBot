import discord 
from discord.ext import commands
import asyncio
import datetime
from discord.ext.commands import MissingPermissions
from discord.ext.commands import *
import time

class ban_unban_kick(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.command(name='kick' , aliases = ['Kick' , 'KICK'])
    @commands.has_permissions(kick_members = True)
    async def kick(self, msg , member:discord.Member, *, reason=None):
        if reason == None : 
            reason = "no reason provided"
        
        await msg.guild.kick(member)
        mbed = discord.Embed(title="Success!",description=f"{member.mention} has been kicked!" , color=discord.Color.random())
        mbed.add_field(name=f"reason : {reason}" , value=" ")
        mbed.set_footer(text=f"command run by : {msg.author}" , icon_url=msg.author.avatar)
        await msg.send(embed=mbed)
        


    #handling errors
    @kick.error
    async def kick_error1(self, msg , error):
        if isinstance(error , MissingPermissions):
                await msg.send("you dont have permission! **[permission require is kick_member = True]**")
    
    @kick.error
    async def kick_error(self, msg , error):
        if isinstance(error , MissingRequiredArgument):
                await msg.send("Missing required argument **[*kick @user reason]**")
     
      

    @commands.command(name='ban' , aliases = ['Ban' , 'BAN'])
    @commands.has_permissions(ban_members = True)
    async def ban(self, msg , member:discord.Member, *, reason=None):
        if reason == None : 
            reason = "no reason provided"
        
        await msg.guild.ban(member)
        mbed = discord.Embed(title="Success!",description=f"{member.mention} has been banned!" , color=discord.Color.random())
        mbed.add_field(name=f"reason : {reason}" , value=" ")
        mbed.set_footer(text=f"command run by : {msg.author}" , icon_url=msg.author.avatar)
        await msg.send(embed=mbed)
        


    #handling errors
    @ban.error
    async def ban_error1(self, msg , error):
        if isinstance(error , MissingPermissions):
                await msg.send("you dont have permission! **[permission require is ban_member = True]**")
    
    @ban.error
    async def ban_error(self, msg , error):
        if isinstance(error , MissingRequiredArgument):
                await msg.send("Missing required argument **[*ban @user reason]**")
     
      

    
    @commands.command(name='unban' , aliases = ['Unban' , 'UNBAN'])
    @commands.has_permissions(ban_members = True)
    async def unban(self, msg , member:discord.User, *, reason=None):
        if reason == None : 
            reason = "no reason provided"
        
        await msg.guild.unban(member)
        mbed = discord.Embed(title="Success!",description=f"{member.mention} has been Unbanned!" , color=discord.Color.random())
        mbed.add_field(name=f"reason : {reason}" , value=" ")
        mbed.set_footer(text=f"command run by : {msg.author}" , icon_url=msg.author.avatar)
        await msg.send(embed=mbed)
        


    #handling errors
    @unban.error
    async def unban_error1(self, msg , error):
        if isinstance(error , MissingPermissions):
                await msg.send("you dont have permission! **[permission require is ban_member = True]**")
    
    @unban.error
    async def unban_error(self, msg , error):
        if isinstance(error , MissingRequiredArgument):
                await msg.send("Missing required argument **[*unban userID reason]**")
     
      
    @commands.command(name='timeout')
    @commands.has_permissions(kick_members=True)
    async def timeout(self, msg , member: discord.Member, seconds: int = 0, minutes: int = 0, hours: int = 0, days: int = 0, reason: str = None):
        if reason == None:
             reason = "no reason provided"

        duration = datetime.timedelta(seconds=seconds, minutes=minutes, hours= hours, days=days)
        await member.timeout(duration, reason=reason)
        mbed = discord.Embed(title="Success!" , description=f"{member.mention} timeouted until next : {duration}" , color=discord.Color.random())
        mbed.add_field(name=f"reason : {reason}" , value=" ")
        mbed.set_footer(text=f"command run by : {msg.author}" , icon_url=msg.author.avatar)
        await msg.send(embed=mbed)
        

async def setup(bot):
    await bot.add_cog(ban_unban_kick(bot))
        