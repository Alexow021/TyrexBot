import discord 
from discord.ext import commands



class latancy(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    #latancy of the bot
    @commands.command(name="ping",aliases = ['latancy','PING','late'])
    async def ping(self, msg):
        await msg.reply(embed = discord.Embed(title="latancy" , description=f"latancy of the bot : {round(self.bot.latency * 1000)}ms <a:botping:1069771709466558514>" , color=discord.Color.random()))



#setting up our cog
async def setup(bot):
    await bot.add_cog(latancy(bot))
