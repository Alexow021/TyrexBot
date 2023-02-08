import discord
from discord.ext import commands


class logger(commands.Cog):
    def __init__(self,bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_member_remove(self, member):
        embed = discord.Embed(title=f"{member} left the {member.guild}" , color=discord.Color.random())
        embed.add_field(name=f"{member.name} joined at {member.joined_at.date()}",value=' ')
        embed.set_thumbnail(url=member.avatar)
        embed.add_field(name=f"is bot ? : " , value=f"{member.bot}",inline= False)
        embed.add_field(name=f"account created at : ", value=f"{member.created_at}", inline= False)
        await self.bot.get_channel(your channel id here).send(f"{member.mention}")
        await self.bot.get_channel(your channel id here).send(embed=embed)





async def setup(bot):
    await bot.add_cog(logger(bot))
