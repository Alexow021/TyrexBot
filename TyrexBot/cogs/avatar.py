import discord 
from discord.ext import commands


#define avatar commands to show users avatar


class Avatar(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.command(name='avatar' , aliases = ['ava'])
    async def avatar(self,msg, member : discord.Member = None):
        if member == None:
            member = msg.author

        userAvatar = member.display_avatar
        embed = discord.Embed(title=f"{member.name}'s Avatar")
        embed.set_image(url=userAvatar)
        embed.set_footer(text = f" request by : {msg.author}" , icon_url=msg.author.avatar)
        await msg.reply(embed = embed)



#setup avatar cog
async def setup(bot):
    await bot.add_cog(Avatar(bot))