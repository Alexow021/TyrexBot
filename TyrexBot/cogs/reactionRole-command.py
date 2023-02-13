import discord
from discord.ext import commands
import asyncio
import json


class ReactionRole(commands.Cog):
    def __init__(self , bot):
        self.bot = bot


    @commands.command(name='rr')
    @commands.has_permissions(manage_messages = True)
    async def self_role(self,ctx):
        await ctx.send("Answer These Question In Next 2Min!")

        questions = ["Enter Message [bot will react this message]: ", "Enter Emojis: [do not send Animated emoji] ", "Enter Roles Names [dont mention roles just their name]: ", "Enter Channel: [use # for tag channel]"]
        answers = []

        def check(user):
            return user.author == ctx.author and user.channel == ctx.channel
        
        for question in questions:
            await ctx.send(question)

            try:
                msg = await self.bot.wait_for('message', timeout=120.0, check=check)
            except asyncio.TimeoutError:
                await ctx.send("Type Faster Next Time!")
                return
            else:
                answers.append(msg.content)

        emojis = answers[1].split(" ")
        roles = answers[2].split(" ")
        c_id = int(answers[3][2:-1])
        channel = self.bot.get_channel(c_id)

        bot_msg = await channel.send(embed = discord.Embed(description=answers[0] , color=discord.Color.random()))

        with open("selfrole.json", "r") as f:
            self_roles = json.load(f)

        self_roles[str(bot_msg.id)] = {}
        self_roles[str(bot_msg.id)]["emojis"] = emojis
        self_roles[str(bot_msg.id)]["roles"] = roles

        with open("selfrole.json", "w") as f:
            json.dump(self_roles, f)

        for emoji in emojis:
            await bot_msg.add_reaction(emoji)

    @self_role.error
    async def self_role_error(msg , error):
            if isinstance(error , commands.MissingPermissions):
                await msg.send("**you dont have permission! [permission require is manage roles]**")
    



    @commands.Cog.listener()
    async def on_raw_reaction_add(self,payload):
        msg_id = payload.message_id

        with open("selfrole.json", "r") as f:
            self_roles = json.load(f)

        if payload.member.bot:
            return
        
        if str(msg_id) in self_roles:
            emojis = []
            roles = []

            for emoji in self_roles[str(msg_id)]['emojis']:
                emojis.append(emoji)

            for role in self_roles[str(msg_id)]['roles']:
                roles.append(role)
            
            guild = self.bot.get_guild(payload.guild_id)
            for i in range(len(emojis)):
                choosed_emoji = str(payload.emoji)
                if choosed_emoji == emojis[i]:
                    selected_role = roles[i]

                    role1 = discord.utils.get(guild.roles , name=selected_role)
                    if role1:
                        await payload.member.add_roles(role1)
                        await payload.member.send(embed = discord.Embed(description=f"You Got **{selected_role}** Role in **{guild}'s server**" , color=discord.Color.random()))
                        

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self,payload):
        msg_id = payload.message_id

        with open("selfrole.json", "r") as f:
            self_roles = json.load(f)
        
        if str(msg_id) in self_roles:
            emojis = []
            roles = []

            for emoji in self_roles[str(msg_id)]['emojis']:
                emojis.append(emoji)

            for role in self_roles[str(msg_id)]['roles']:
                roles.append(role)
            
            guild = self.bot.get_guild(payload.guild_id)

            for i in range(len(emojis)):
                choosed_emoji = str(payload.emoji)
                if choosed_emoji == emojis[i]:
                    selected_role = roles[i]

                    role = discord.utils.get(guild.roles, name=selected_role)

                    member = await(guild.fetch_member(payload.user_id))
                    if member is not None:
                        await member.remove_roles(role)



#setting up our cog
async def setup(bot):
    await bot.add_cog(ReactionRole(bot))




