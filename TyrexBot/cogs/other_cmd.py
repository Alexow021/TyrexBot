import discord
from discord.ext import commands


class otherCmd(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    
    @commands.command(name='other',aliases =['Other' , 'OTHER'])
    async def other(self,msg):
        embed = discord.Embed(title=f"Ty-Rex Bot" , color=discord.Color.random())
        embed.add_field(name='*ping' , value='latancy of the bot')
        embed.add_field(name='*avatar [USER]' , value='Display users avatar')
        embed.add_field(name='*clear' , value='clear messages only if you have perm [manage messages]')
        embed.add_field(name='*rr' , value="create reaction roles only if you have perm [manage roles]")
        embed.set_thumbnail(url='https://images-ext-2.discordapp.net/external/8Qg_eMgPsh5CreEFw-pvmAaumxC7CPS5SNVmd0i6fI4/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/1053389952634855475/c2266b5f45dbeec4594e57f799776c73.png?width=683&height=683')

        await msg.send(embed = embed)


async def setup(bot):
    await bot.add_cog(otherCmd(bot))
