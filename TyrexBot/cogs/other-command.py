import discord 
from discord.ext import commands


class otherCmd(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.command(name='other')
    async def otherCmd(self , msg):
        embed = discord.Embed(title='**other command menu**' , color=discord.Color.random())
        embed.add_field(name='*rr' , value='for create reaction role [require manage roles permission]' , inline=True)
        embed.add_field(name='*ping' , value='for get latancy of the bot', inline=False)
        embed.add_field(name='*avatar [mention user]' , value='for displaying users avatar', inline=False)
        embed.add_field(name='*fact' , value='get a random fact', inline=False)
        embed.add_field(name="*free" , value="free games on the Epic store!")
        embed.add_field(name='*clear [number]' , value='for clearing messages [require manage messages permission]' , inline=False)
        embed.add_field(name='*kick @user reason' , value='kick members [require kick_member permission]' , inline=False)
        embed.add_field(name='*ban @user reason' , value='ban members [require ban_member permission]' , inline=False)
        embed.add_field(name='*unban userID reason' , value='unban members [require ban_member permission]' , inline=False)
        await msg.send(embed=embed)





async def setup(bot):
    await bot.add_cog(otherCmd(bot))
        