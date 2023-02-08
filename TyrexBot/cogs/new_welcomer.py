import discord
from discord.ext import commands


class welcomer(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    #auto role 
    @commands.Cog.listener()
    async def on_member_join(self, member):
        roles = [
            #paste your role id here 
            1070169989501436084, #extra               ''' write your server id role here'''
            1070168559042449480, #general
            1070170334411640944, #lang
            1070168757688881292, #pro lang
            1070167847176769606 #perm
        ]

        for id in roles : 
            giveRole = discord.utils.get(member.guild.roles , id = id)
            if giveRole:
                await member.add_roles(giveRole)


        #welcomer
        ch = await self.bot.fetch_channel(your channel id here) #your channel id here
        embed = discord.Embed(title="Welcome to the Club :slight_smile:" , color=discord.Color.random())
        embed.add_field(name=f"{member} joined at {member.joined_at.date()}" , value="feel free in our server to get help use: ```*help```")
        embed.add_field(name=f" " , value=f"from {ch.mention} choose your languege",inline= False)
        embed.set_thumbnail(url=member.avatar)
        embed.add_field(name=f"is bot ? : " , value=f"{member.bot}",inline= False)
        embed.add_field(name=f"account created at : ", value=f"{member.created_at}", inline= False)
        await self.bot.get_channel(your channel id here).send(f"{member.mention}") #your channel id here
        await self.bot.get_channel(your channel id here).send(embed = embed) #your channel id here



async def setup(bot):
    await bot.add_cog(welcomer(bot))
