from discord.ext import commands

from extensions.base_cog import BaseCog
from essentials.music.musicbot import MusicBot
from utils.embeds import QueueEmbed
from utils.logger import Logger


class Music(BaseCog):
    # TO DO:
    # EVERY SINGLE COMMAND SHOULD RETURN IF THE BOT CANT SEND MESSAGES TO THE CURRENT CHANNEL
    def __init__(self, bot) -> None:
        super().__init__(bot)
        self._music_bot = MusicBot(bot)

    @commands.command()
    async def connect(self, ctx):
        await self._music_bot.connect(ctx)

    @commands.command()
    async def disconnect(self, ctx):
        await self._music_bot.disconnect(ctx)
    
    @commands.command()
    async def play(self, ctx, url, *args):
        await self._music_bot.play(ctx, url, *args)

    @commands.command()
    async def skip(self, ctx):
        await self._music_bot.skip(ctx)

    @commands.command()
    async def loop(self, ctx):
        await self._music_bot.loop(ctx)

    @commands.command()
    async def nowplaying(self, ctx):
        await self._music_bot.now_playing(ctx)

    @commands.command()
    async def pause(self, ctx):
        await self._music_bot.pause(ctx)

    @commands.command()
    async def remove(self, ctx, index):
        await self._music_bot.remove(ctx, index)

    @commands.command()
    async def nightcore(self, ctx):
        await self._music_bot.nightcore(ctx)
    
    @commands.command()
    async def daycore(self, ctx):
        await self._music_bot.daycore(ctx)

    @commands.command()
    async def setspeed(self, ctx, speed):
        await self._music_bot.setspeed(ctx, speed)

    @commands.command()
    async def resetspeed(self, ctx):
        await self._music_bot.resetspeed(ctx)

    @commands.command()
    async def previous(self, ctx):
        await self._music_bot.previous(ctx)

    @commands.command()
    async def lyrics(self, ctx, *song_title):
        await self._music_bot.lyrics(ctx, song_title)

    @commands.command()
    async def shuffle(self, ctx):
        await self._music_bot.shuffle(ctx)
    
    @commands.command()
    async def queue(self, ctx):
        await self._music_bot.queue(ctx)

    @commands.command()
    async def bassboost(self, ctx):
        await self._music_bot.bassboost(ctx)

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if member.id != member.guild.me.id:
            return
        if after.channel is None and self._music_bot.get_server(member.guild.id):
            Logger.warning(f'Force disconnect on {member.guild.id} server!')
            self._music_bot.clear_server(member.guild.id)
        if after.channel is not None and before.channel is not None:
            Logger.warning(f'Bot has been force moved from {before.channel.id} to {after.channel.id}')
            self._music_bot.update_voice_channel(member.guild.id, after.channel)
    
    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel):
        guild = channel.guild
        music_bot_chache = self._music_bot.get_server(guild.id)
        if not music_bot_chache:
            return
        if channel.id != music_bot_chache['text_channel'].id:
            return
        self._music_bot.clear_text_channel()

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if user.id == self.bot.user.id:
            return
        server = self._music_bot.get_server(reaction.message.guild.id)
        if not server:
            return
        if reaction.message != server['queue_message']:
            return
        if reaction.emoji not in QueueEmbed.REACTIONS:
            return
        try:
            ctx = server['queue_context']
        except Exception:
            ctx = None
        if ctx is None:
            return
        try:
            audio_player = server['audio_player']
        except Exception:
            audio_player = None
        if audio_player is None:
            return
        if reaction.emoji == QueueEmbed.REACTIONS[0]:
            audio_player.decrement_page()
        if reaction.emoji == QueueEmbed.REACTIONS[1]:
            audio_player.increment_page()
        await self.queue(ctx)

def setup(client):
    client.add_cog(Music(client))