import discord
from discord.ext import commands
import requests
import json

class epicGames(commands.Cog):
    def __init__(self , bot):
        self.bot = bot

    @commands.command(name='free', pass_context=True)
    async def free(self , ctx):
    
        try:
            ENDPOINT = "https://store-site-backend-static.ak.epicgames.com/freeGamesPromotions?locale=es-ES&country=ES&allowCountries=ES"
            URL = "https://store.epicgames.com/en-US/p/"
            raw_data = requests.get(ENDPOINT)
            raw_data = json.loads(raw_data.content) 
            raw_data = raw_data["data"]["Catalog"]["searchStore"]["elements"]  # Cleans the data
            processed_data = []
            for i in raw_data:
                            try:
                                if i["promotions"]["promotionalOffers"]:
                                    
                                    game = i['keyImages'][1]['url']
                                    
                                    processed_data.append(game)
                            except TypeError:
                                pass

            for i in raw_data:
                try:
                    if i["promotions"]["promotionalOffers"]:
                        
                        game = i['title']                      
                        processed_data.append(game)
                except TypeError:
                    pass

            for i in raw_data:
                try:
                    if i["promotions"]["promotionalOffers"]:
                        
                        game = i['price']['totalPrice']['fmtPrice']['originalPrice']
                        
                        processed_data.append(game)
                        
                except Exception as e:
                    print(e)
            
            for i in raw_data:
                try:
                    if i["promotions"]["promotionalOffers"]:
                        
                        game = i['catalogNs']['mappings'][0]['pageSlug']
                        processed_data.append(game)
                except TypeError:
                    pass
            for i in raw_data:
                try:
                    if i["promotions"]["promotionalOffers"]:
                        
                        game = i['promotions']['promotionalOffers'][0]['promotionalOffers'][0]['startDate']
                        processed_data.append(game)
                except TypeError:
                    pass
            for i in raw_data:
                try:
                    if i["promotions"]["promotionalOffers"]:
                        
                        game = i['promotions']['promotionalOffers'][0]['promotionalOffers'][0]['endDate']
                        processed_data.append(game)
                except TypeError:
                    pass
            
            embed = discord.Embed(title=f"{processed_data[1]} is now free on the Epic store!"  , url=URL+processed_data[3] , color=discord.Color.random())
            embed.add_field(name=f"~~{processed_data[2]}~~ -> Free" , value=" " , inline=False)
            embed.add_field(name=f"<a:everythingisstable:1065398972379824220> StartDate : {processed_data[4][:-14]}" , value=" " , inline=False)
            embed.add_field(name=f"<a:laydowntorest:1065398993091317920> EndDate : {processed_data[5][:-14]}" , value=" ")
            embed.set_image(url=processed_data[0])
            await ctx.send(embed = embed)

        except Exception:
            
            pass


async def setup(bot):
    await bot.add_cog(epicGames(bot))