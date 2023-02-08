###############################################################################################
# module for all embeds
###############################################################################################

from discord import Embed, Colour
import discord


# returns the currently playing song as an embed in channel
def nowPlayingEmbed(ctx, entry):
    import datetime
    try:
        # outer scope, check if there even is a song in the queue
        if entry:
            # check if item in self.queue[0] is a playlist
            if 'playlist' in entry:
                embed = Embed(title=entry['title'], color=discord.Color.random(), url=entry['url'])
                embed.add_field(name='Track: ', value=entry['songs'][0]['title'], inline=True)
                embed.set_thumbnail(url=entry['songs'][0]['thumbnail'])
                embed.add_field(name='Requested by:', value=ctx.author.display_name, inline=False)
                embed.add_field(name='Duration:', value=str(datetime.timedelta(seconds=entry['songs'][0]['duration'])), inline=True)
                
                return embed
            # if not, continue as normal
            else:    
                embed = Embed(title=entry['title'], color=discord.Color.random(), url=entry['webpage_url'])
                embed.set_thumbnail(url=entry['thumbnail'])
                embed.add_field(name='Requested by:', value=ctx.author.display_name)
                embed.add_field(name='Duration:', value=str(datetime.timedelta(seconds=entry['duration'])), inline=True)
                
                return embed
        else:
            embed = Embed(title='No song', color=discord.Color.random())
            
            return embed 
    except IndexError:
        embed = Embed(title='No song', color=discord.Color.random())
        
        return embed 


# an embed that provides all entries in a entry, proliferates on all of "entry's" entries
def queueEmbed(entry):
    if entry:
        embed = Embed(title='Queue', color=discord.Color.random())
        num = 1
        for item in entry:
            if 'playlist' in item:
                    embed.add_field(name='Playlist', value=item['title'], inline=False)
                    embed.add_field(name='Tracks: ', value=str(len(item['songs'])))
                    num += 1
            else:
                embed.add_field(name='Track ' + str(num), value=item['title'], inline=False)
                num += 1
            # mandatory cap for discord message limit
            if num == 200:
                embed.add_field(name='Max reached', value='More in queue')
                break

        
        return embed
    else:
        embed = Embed(title='No queue', color=discord.Color.random())
    
        return embed 

# an embed for skipped song
def skipEmbed(entry, ctx):
    import datetime
    if entry:
        if 'playlist' in entry[0]:
            embed = Embed(title=entry[0]['title'], color=discord.Color.random(), url=entry[0]['url'])
            embed.add_field(name='Skipping: ', value=entry[0]['songs'][0]['title'])
            embed.add_field(name='Skipped by:', value=ctx.author.display_name)        
            embed.add_field(name='Duration:', value=str(datetime.timedelta(seconds=entry[0]['songs'][0]['duration'])), inline=True)
            embed.set_thumbnail(url=entry[0]['songs'][0]['thumbnail'])
            
            return embed
        else:
            embed = Embed(color=discord.Color.random())
            embed.add_field(name='Skipping: ', value=entry[0]['title'])
            embed.add_field(name='Skipped by:', value=ctx.author.display_name)        
            embed.add_field(name='Duration:', value=str(datetime.timedelta(seconds=entry[0]['duration'])), inline=True)
            embed.set_thumbnail(url=entry[0]['thumbnail'])
            
            return embed 
    if not entry:
        embed = Embed(title='No entry', color=discord.Color.random())
        
        return embed

def repeatEmbed(entry, ctx):
    import datetime
    if entry:
        if 'playlist' in entry[0]:
            embed = Embed(color=discord.Color.random())
            embed.add_field(name='Repeating: ', value=entry[0]['songs'][0]['title'])
            embed.add_field(name='Requested by:', value=ctx.author.display_name)
            embed.add_field(name='Duration:', value=str(datetime.timedelta(seconds=entry[0]['songs'][0]['duration'])), inline=True)
            embed.set_thumbnail(url=entry[0]['songs'][0]['thumbnail'])
            
            return embed 
        else:
            embed = Embed(color=discord.Color.random())
            embed.add_field(name='Repeating: ', value=entry[0]['title'])
            embed.add_field(name='Requested by:', value=ctx.author.display_name)
            embed.add_field(name='Duration:', value=str(datetime.timedelta(seconds=entry[0]['duration'])), inline=True)
            embed.set_thumbnail(url=entry[0]['thumbnail'])
            return embed
    else:
        embed = Embed(title='No entry', color=discord.Color.random())

        return embed  


def everyBodyLeft():
    embed = Embed(color=discord.Color.random())
    embed.add_field(name= " " , value='Disconnected ,if you need me just call me <a:pepejam:1066878076576858163>')

    return embed




def inactivty():
    embed = Embed(color=discord.Color.random())
    embed.add_field(name=" " , value="Disconnected due to inactivity. for more join our discord server.")

    return embed