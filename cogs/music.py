import discord
from discord.ext import commands
from cogs.base_cog import BaseCog
from utils.musicbot import MusicBot
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

def setup(client):
    client.add_cog(Music(client))