import discord
from discord.ext import commands
from cogs.base_cog import BaseCog
from utils.musicbot import MusicBot


class Music(BaseCog):
    def __init__(self, bot) -> None:
        super().__init__(bot)
        self._music_bot = MusicBot(bot)

    @commands.command()
    async def connect(self, ctx):
        await self._music_bot.connect(ctx)

    @commands.command()
    async def disconnect(self, ctx):
        await self._music_bot.disconnect(ctx)

def setup(client):
    client.add_cog(Music(client))