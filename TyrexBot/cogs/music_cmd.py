import discord
from discord.ext import commands


class musicCmd(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    
    #you can customize here 
    @commands.command(name='music',aliases = ['Music','MUSIC'])
    async def music(self,msg):
        embed = discord.Embed(title=f"Ty-Rex Bot" , color=discord.Color.random())
        embed.add_field(name='*play',value='for playing music [auto queue]')
        embed.add_field(name='*stop',value='for stop music and cleaning the queue [bot will be dissconnected]' , inline=False)
        embed.add_field(name='*pause',value='for pause the song')
        embed.add_field(name='*resume',value='for resume the song')
        embed.add_field(name='*queue' , value='Display queue of upcoming songs')
        embed.add_field(name='*np',value='Display information about the currently playing song')
        embed.add_field(name='*skip',value='for skip song')
        embed.add_field(name='*clearsongs' , value='for clearing the queue')
        embed.set_thumbnail(url='https://images-ext-2.discordapp.net/external/8Qg_eMgPsh5CreEFw-pvmAaumxC7CPS5SNVmd0i6fI4/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/1053389952634855475/c2266b5f45dbeec4594e57f799776c73.png?width=683&height=683')

        await msg.send(embed = embed)


async def setup(bot):
    await bot.add_cog(musicCmd(bot))
