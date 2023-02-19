import discord 
from discord.ext import commands
import requests


class nude(commands.Cog):
    def __init__(self,bot):
        self.bot = bot


    @commands.command(name='nude' , pass_context=True)
    async def nude(self , msg , search : str):
        if msg.channel.is_nsfw():
            if search == "ass" : 
                r = requests.get("https://api.waifu.im/search/?included_tags=ass")
                res = r.json()
                em = discord.Embed(color=discord.Color.random())
                em.set_footer(text = f'requested by {msg.author}' , icon_url=f"{msg.author.avatar}")
                em.set_image(url=res['images'][0]['url'])
                await msg.send(embed=em)
            else : 
                pass
            if search == "milf" : 
                r = requests.get("https://api.waifu.im/search/?included_tags=milf")
                res = r.json()
                em = discord.Embed(color=discord.Color.random())
                em.set_footer(text = f'requested by {msg.author}' , icon_url=f"{msg.author.avatar}")
                em.set_image(url=res['images'][0]['url'])
                await msg.send(embed=em)
            else : 
                pass
            if search == "oral" : 
                r = requests.get("https://api.waifu.im/search/?included_tags=oral")
                res = r.json()
                em = discord.Embed(color=discord.Color.random())
                em.set_footer(text = f'requested by {msg.author}' , icon_url=f"{msg.author.avatar}")
                em.set_image(url=res['images'][0]['url'])
                await msg.send(embed=em)
            else : 
                pass
            if search == "ero" : 
                r = requests.get("https://api.waifu.im/search/?included_tags=ero")
                res = r.json()
                em = discord.Embed(color=discord.Color.random())
                em.set_footer(text = f'requested by {msg.author}' , icon_url=f"{msg.author.avatar}")
                em.set_image(url=res['images'][0]['url'])
                await msg.send(embed=em)
            else : 
                pass
            if search == "hentai" : 
                r = requests.get("https://api.waifu.im/search/?included_tags=hentai")
                res = r.json()
                em = discord.Embed(color=discord.Color.random())
                em.set_footer(text = f'requested by {msg.author}' , icon_url=f"{msg.author.avatar}")
                em.set_image(url=res['images'][0]['url'])
                await msg.send(embed=em)
            else : 
                pass

            if search == "paizuri" : 
                r = requests.get("https://api.waifu.im/search/?included_tags=paizuri")
                res = r.json()
                em = discord.Embed(color=discord.Color.random())
                em.set_footer(text = f'requested by {msg.author}' , icon_url=f"{msg.author.avatar}")
                em.set_image(url=res['images'][0]['url'])
                await msg.send(embed=em)
            else : 
                pass


            if search == "ecchi" : 
                r = requests.get("https://api.waifu.im/search/?included_tags=ecchi")
                res = r.json()
                em = discord.Embed(color=discord.Color.random())
                em.set_footer(text = f'requested by {msg.author}' , icon_url=f"{msg.author.avatar}")
                em.set_image(url=res['images'][0]['url'])
                await msg.send(embed=em)
            else : 
                pass
        else:
            await msg.send("**this isn't nsfw channel use this command in a nsfw channel!**")


async def setup(bot):
    await bot.add_cog(nude(bot))
        