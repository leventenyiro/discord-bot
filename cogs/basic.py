from operator import contains
import discord
from discord.ext import commands
from cogs.base_cog import BaseCog
from spotify.spotify import Spotify

class Basic(BaseCog):
    def __init__(self, bot) -> None:
        super().__init__(bot)

    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f'Pong! {round(self.bot.latency*1000)} ms')

    @commands.command()
    async def play(self, ctx, arg):
        # Spotify recognization
        if (contains(arg, 'spotify')):
            # Teszt
            await ctx.send(Spotify.get_track(arg))
            # Itt küldi a kérelmet a youtube modulenak
            # Spotify.get_track(arg)

def setup(client):
    client.add_cog(Basic(client))