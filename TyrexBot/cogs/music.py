import discord
from discord.ext import commands
import asyncio
import itertools
import sys
import traceback
from async_timeout import timeout
from functools import partial
from youtube_dl import YoutubeDL
from youtube_dl.utils import DownloadError


ytdlopts = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    #'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0'  # ipv6 addresses cause issues sometimes
}

ffmpegopts = {
    'before_options': '-nostdin',
    'options': '-vn'
}

ytdl = YoutubeDL(ytdlopts)


class VoiceConnectionError(commands.CommandError):
    """Custom Exception class for connection errors."""


class InvalidVoiceChannel(VoiceConnectionError):
    """Exception for cases of invalid Voice Channels."""


class YTDLSource(discord.PCMVolumeTransformer):

    def __init__(self, source, *, data, requester):
        super().__init__(source)
        self.requester = requester

        self.title = data.get('title')
        self.web_url = data.get('webpage_url')

    def __getitem__(self, item: str):
        return self.__getattribute__(item)

    @classmethod
    async def create_source(cls, ctx, search: str, *, loop, download=False):
        loop = loop or asyncio.get_event_loop()

        to_run = partial(ytdl.extract_info, url=search, download=download)
        data = await loop.run_in_executor(None, to_run)

        if 'entries' in data:
            data = data['entries'][0]

        await ctx.reply(f'Added to the Queue.', delete_after=5)
        

        if download:
            source = ytdl.prepare_filename(data)
        else:
            return {'webpage_url': data['webpage_url'], 'requester': ctx.author, 'title': data['title']}

        return cls(discord.FFmpegPCMAudio(source), data=data, requester=ctx.author)

    @classmethod
    async def regather_stream(cls, data, *, loop):
       
        loop = loop or asyncio.get_event_loop()
        requester = data['requester']

        to_run = partial(ytdl.extract_info, url=data['webpage_url'], download=False)
        data = await loop.run_in_executor(None, to_run)

        return cls(discord.FFmpegPCMAudio(data['url']), data=data, requester=requester)


class MusicPlayer():

    __slots__ = ('bot', '_guild', '_channel', '_cog', 'queue', 'next', 'current', 'np', 'volume')

    def __init__(self, ctx):
        self.bot = ctx.bot
        self._guild = ctx.guild
        self._channel = ctx.channel
        self._cog = ctx.cog

        self.queue = asyncio.Queue()
        self.next = asyncio.Event()

        self.np = None  # Now playing message
        self.volume = .5
        self.current = None

        ctx.bot.loop.create_task(self.player_loop())

    async def player_loop(self):
        await self.bot.wait_until_ready()

        while not self.bot.is_closed():
            self.next.clear()

            try:
                async with timeout(300):  # 5 minutes...
                    source = await self.queue.get()
            except asyncio.TimeoutError:
                return self.destroy(self._guild)

            if not isinstance(source, YTDLSource):
                try:
                    source = await YTDLSource.regather_stream(source, loop=self.bot.loop)
                except Exception as e:
                    await self._channel.send(f'There was an error processing your song. <:sadge:1065396073666981908> try again!')
                    continue

            source.volume = self.volume
            self.current = source
            self._guild.voice_client.play(source, after=lambda _: self.bot.loop.call_soon_threadsafe(self.next.set))
            self.np = await self._channel.send(embed = discord.Embed(description=f"<a:musicplaying:1069771651568381973> Now Playing: {source.title}"))
            await self.next.wait()

            # Make sure the FFmpeg process is cleaned up.
            source.cleanup()
            self.current = None

            try:
                # We are no longer playing this song...
                await self.np.delete()
            except discord.HTTPException:
                pass

    def destroy(self, guild):
        """Disconnect and cleanup the player."""
        return self.bot.loop.create_task(self._cog.cleanup(guild))


class Music(commands.Cog):
    """Music related commands."""

    __slots__ = ('bot', 'players')

    def __init__(self, bot):
        self.bot = bot
        self.players = {}
        self.chatChannel = False

    async def cleanup(self, guild):
        try:
            await guild.voice_client.disconnect()
        except AttributeError:
            pass

        try:
            del self.players[guild.id]
        except KeyError:
            pass

    async def __local_check(self, ctx):
        """A local check which applies to all commands in this cog."""
        if not ctx.guild:
            raise commands.NoPrivateMessage
        return True

    async def __error(self, ctx, error):
        """A local error handler for all errors arising from commands in this cog."""
        if isinstance(error, commands.NoPrivateMessage):
            try:
                return await ctx.send('This command can not be used in Private Messages!!')
            except discord.HTTPException:
                pass
        elif isinstance(error, InvalidVoiceChannel):
            await ctx.send('Error connecting to Voice Channel.')

        print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

    def get_player(self, ctx):
        try:
            player = self.players[ctx.guild.id]
        except KeyError:
            player = MusicPlayer(ctx)
            self.players[ctx.guild.id] = player

        return player

    @commands.command(name='join', aliases=['j' , 'JOIN' , "Join" , 'J'])
    async def connect_(self, ctx, *, channel: discord.VoiceChannel=None):
        if not channel:
            try:
                channel = ctx.author.voice.channel
            except AttributeError:
                raise InvalidVoiceChannel('please first join a voice channel')

        vc = ctx.voice_client

        if vc:
            if vc.channel.id == channel.id:
                return
            try:
                await vc.move_to(channel)
            except asyncio.TimeoutError:
                raise VoiceConnectionError(f'Moving to channel: <{channel}> timed out.')
        else:
            try:
                await channel.connect()
                self.chatChannel = ctx.message.channel.id
                await ctx.send(f'Connected to: **{channel}**', delete_after=2)

            except asyncio.TimeoutError:
                raise VoiceConnectionError(f'Connecting to channel: <{channel}> timed out.')


    @commands.command(name='play', aliases=['sing' , 'p' , 'Play' , 'PLAY' ,'P'])
    async def play_(self, ctx, *, search: str):
        
        vc = ctx.voice_client

        if not vc:
            await ctx.invoke(self.connect_)

        player = self.get_player(ctx)

        source = await YTDLSource.create_source(ctx, search, loop=self.bot.loop, download=False)

        await player.queue.put(source)
        self.chatChannel = ctx.message.channel.id 

    @commands.command(name='pause' , aliases = ['ps' ,'Pause' , 'PAUSE'])
    async def pause_(self, ctx):
        """Pause the currently playing song."""
        vc = ctx.voice_client

        if not vc or not vc.is_playing():
            return await ctx.send('I am not currently playing anything!', delete_after=2)
        elif vc.is_paused():
            return

        vc.pause()
        await ctx.send(f'**{vc.source.requester.display_name}** Paused the song!')

    @commands.command(name='resume',aliases = ['rs' , 'Resume' , 'RESUME'])
    async def resume_(self, ctx):
        """Resume the currently paused song."""
        vc = ctx.voice_client

        if not vc or not vc.is_connected():
            return await ctx.send('I am not currently playing anything!', delete_after=2)
        elif not vc.is_paused():
            return

        vc.resume()
        await ctx.send(f'**{vc.source.requester.display_name}** Resumed the song!')

    @commands.command(name='skip' , aliases = ['s'])
    async def skip_(self, ctx):
        """Skip the song."""
        vc = ctx.voice_client

        if not vc or not vc.is_connected():
            return await ctx.send('I am not currently playing anything!', delete_after=2)

        if vc.is_paused():
            pass
        elif not vc.is_playing():
            return

        vc.stop()
        await ctx.send(f'Skipped the song!')

    @commands.command(name='queue', aliases=['q', 'Q' , 'Queue' , 'QUEUE'])
    async def queue_info(self, ctx):
        """Retrieve a basic queue of upcoming songs."""
        vc = ctx.voice_client

        if not vc or not vc.is_connected():
            return await ctx.send('I am not currently connected to voice!', delete_after=2)

        player = self.get_player(ctx)
        if player.queue.empty():
            return await ctx.send('There are currently no more queued songs.')

        # Grab up to 5 entries from the queue...
        upcoming = list(itertools.islice(player.queue._queue, 0, 5))

        fmt = '\n'.join(f'**`{_["title"]}`**' for _ in upcoming)
        embed = discord.Embed(title=f'Upcoming - Next {len(upcoming)}', description=fmt , color=discord.Color.random())

        await ctx.send(embed=embed)

    @commands.command(name='nowPlaying', aliases=['np', 'current', 'currentsong', 'playing'])
    async def now_playing_(self, ctx):
        """Display information about the currently playing song."""
        vc = ctx.voice_client

        if not vc or not vc.is_connected():
            return await ctx.send('I am not currently connected to voice!', delete_after=2)

        player = self.get_player(ctx)
        if not player.current:
            return await ctx.send('I am not currently playing anything!')

        try:
            # Remove our previous now_playing message.
            await player.np.delete()
        except discord.HTTPException:
            pass

        em = discord.Embed(description=f"<a:musicplaying:1069771651568381973> Now Playing: {vc.source.title}" , color=discord.Color.random())
        em.add_field(name=f'<a:url:1066876243263365220> url: {vc.source.web_url}' , value=" ")
        em.set_footer(text=f'requested by : {vc.source.requester}' , icon_url=vc.source.requester.avatar)
        player.np = await ctx.send(embed = em)
                                   

    @commands.command(name='volume', aliases=['vol'])
    async def change_volume(self, ctx, *, vol: float):
        vc = ctx.voice_client

        if not vc or not vc.is_connected():
            return await ctx.send('I am not currently connected to voice!', delete_after=2)

        if not 0 < vol < 101:
            return await ctx.send('Please enter a value between 1 and 100.')

        player = self.get_player(ctx)

        if vc.source:
            vc.source.volume = vol / 100

        player.volume = vol / 100
        await ctx.send(f'Set the volume to **{vol}%**')

    @commands.command(name='stop')
    async def stop_(self, ctx):
        vc = ctx.voice_client

        if not vc or not vc.is_connected():
            return await ctx.send('I am not currently playing anything!', delete_after=2)

        await self.cleanup(ctx.guild)


    
    @play_.before_invoke
    async def confirmQuery(self, ctx):
        if not ctx.args:
            raise commands.MissingRequiredArgument

      
    # -play yields a variety of errors out of CommandInvokeError. localize for each 
    @play_.error
    async def playError(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            # throw if user is trying to use -play to queue a playlist
            if isinstance(error.original, IndexError):
                await ctx.send('Something went wrong. If you are trying to queue a playlist, try the "*playlist" command with a link to the playlist.')
            # if the query fails
            if isinstance(error.original, (DownloadError)):
                await ctx.send('Something went wrong. Try again.')    
            # if the user is not in a channel
            if isinstance(error.original, AttributeError):
                await ctx.send('Something went wrong. Try again.')
        
        # from pre-invoke; throw if user sends an empty command
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('You have to pass something in with the *play command.')
        else:
            raise

    @pause_.error
    async def pauseError(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            # if user tries to pause the bot when not paused
            if isinstance(error.original, AttributeError):
                await ctx.send('I am not currently connected.')
        else:
            raise

    
    @skip_.error
    async def skipError(self, ctx, error):
        if isinstance(error, AttributeError):
            if isinstance(error.original, AttributeError):
                await ctx.send('You\'re not in a voice.')
        else:
            raise
    
        
        
        
        
        
    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        # if all members of voice channel leave, leave as well
        voice = member.guild.voice_client 
        # check to see if the bot is alone
        if voice is not None and len(voice.channel.members) == 1: 
            await voice.disconnect()
            ctxChannel = self.bot.get_channel(self.chatChannel)
            
            await ctxChannel.send(embed = discord.Embed(description="everybody left , **disconnected!**"))
          
        # disconnect if idle
        if not member.id == self.bot.user.id:
            return
        elif before.channel is None:
            voice = after.channel.guild.voice_client
            time = 0
            while True:
                await asyncio.sleep(1)
                time = time + 1
                # reset if playing and not paused, or reset if paused
                if (voice.is_playing() and not voice.is_paused()):
                    time = 0
                elif voice.stop() == True or voice.pause() == True:
                    pass
                if time == 60:
                    await voice.disconnect()
                    ctxChannel = self.bot.get_channel(self.chatChannel)
                    await ctxChannel.send(embed = discord.Embed(description="**disconnected due to inactivty**"))
                if not voice.is_connected():
                    break        
    


async def setup(bot):
    await bot.add_cog(Music(bot))
