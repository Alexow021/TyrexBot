import discord 
from discord.ext import commands


class musicCmd(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.command(name='music')
    async def musicCmd(self , msg):
        embed = discord.Embed(title='**Music command menu**' , color=discord.Color.random())
        embed.add_field(name='*play' , value='playing music from youtube or soundcloud or any http/https link' , inline=True)
        embed.add_field(name='*queue' , value='displaying upcoming msuic', inline=False)
        embed.add_field(name='*skip' , value='skip music', inline=False)
        embed.add_field(name='*stop' , value='stop music', inline=False)
        embed.add_field(name='*pause' , value='pause music' , inline=False)
        embed.add_field(name='*resume' , value='resume music', inline=False)
        embed.add_field(name='*nowPlaying' , value='Now Playing', inline=False)
        embed.add_field(name='*vol [number]' , value='changeing volume', inline=False)
        await msg.send(embed=embed)





async def setup(bot):
    await bot.add_cog(musicCmd(bot))
        