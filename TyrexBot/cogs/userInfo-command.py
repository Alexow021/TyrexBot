import discord
from discord.ext import commands



class userInfo(commands.Cog):
    def __init__(self,bot):
        self.bot = bot


    @commands.command(name='user')
    async def userinfo(self , ctx, user: discord.Member = None): # b'\xfc'
        if user is None:
            user = ctx.author      
        date_format = "%a, %d %b %Y %I:%M %p"
        embed = discord.Embed(color=0xdfa3ff)
        embed.set_author(name=str(user), icon_url=user.avatar)
        embed.set_thumbnail(url=user.avatar)
        embed.add_field(name="Joined", value=user.joined_at.strftime(date_format))
        members = sorted(ctx.guild.members, key=lambda m: m.joined_at)
        embed.add_field(name="Join position", value=str(members.index(user)+1))
        embed.add_field(name="Registered", value=user.created_at.strftime(date_format))
        if len(user.roles) > 1:
            role_string = ' \n'.join([r.mention for r in user.roles][1:])
            embed.add_field(name=f"[Roles {len(user.roles)-1}]", value=f'{role_string}', inline=False)
        perm_string = '\n'.join([str(p[0]).replace("_", " ").title() for p in user.guild_permissions if p[1]])
    
        if user.guild_permissions.administrator: 
            
            embed.add_field(name="[Guild permissions]", value=f'```Administrator```', inline=False)
        else :
            
            embed.add_field(name="[Guild permissions]", value=f'```{perm_string}```', inline=False)
        embed.set_footer(text='ID: ' + str(user.id))
        return await ctx.send(embed=embed)

    





async def setup(bot):
    await bot.add_cog(userInfo(bot))