import discord
from discord.ext import commands
import requests

class fact(commands.Cog):
    def __init__(self , bot):
        self.bot = bot

    
    @commands.command(name='fact')
    async def fact(self , msg):
        r = requests.get("https://nekos.life/api/v2/fact")
        res = r.json()
        em = discord.Embed(color=discord.Color.random())
        em.add_field(name="**fact : **" , value=f"{res['fact']}")
        em.set_footer(text=f"requested by {msg.author}" , icon_url=f"{msg.author.avatar}")
        await msg.send(embed=em)


async def setup(bot):
    await bot.add_cog(fact(bot))