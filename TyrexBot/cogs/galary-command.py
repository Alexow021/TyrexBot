import discord 
from discord.ext import commands


class galary(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.command(name='galary')
    async def galary(self , msg):
        embed = discord.Embed(title='**galary menu**' , color=discord.Color.random())
        embed.add_field(name='*nude [milf , ass , ero , ecchi , hentai , paizuri , oral]',value="<:nsfwchannel:1075309235765776424> Display nsfw content"  , inline=False)
        await msg.send(embed=embed)





async def setup(bot):
    await bot.add_cog(galary(bot))
        