import discord 
from discord.ext import commands



class latancy(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    #latancy of the bot
    @commands.command(name="ping",aliases = ['latancy','PING','late'])
    async def ping(self, msg):
        await msg.reply(embed = discord.Embed(title="latancy :satellite:" , description=f"latancy of the bot : {round(self.bot.latency * 1000)}ms" , color=discord.Color.random()))



async def setup(bot):
    await bot.add_cog(latancy(bot))