import discord
from discord.ext import commands


#define info commands to show other commands


class help(commands.Cog):
    def __init__(self , bot):
        self.bot = bot

    #you can customize here 
    @commands.command(name='help' , aliases = ['INFO' , 'Info' , 'Help' , 'HELP'])
    async def help(self,msg):
        embed = discord.Embed(title=f"Ty-Rex Bot" , color=discord.Color.random())
        embed.add_field(name='*music' , value='<a:musicplaying:1069771651568381973> Display information about music commands')
        embed.add_field(name='*other',value="<:commands:1067925738596081765> Display other commands" , inline=False)
        embed.add_field(name='*galary',value="<:picture:1075288458907615312> Display galary commands"  , inline=False)
        await msg.reply(embed = embed)





#setting up our cog
async def setup(bot):
    await bot.add_cog(help(bot))


