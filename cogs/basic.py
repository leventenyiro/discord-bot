from operator import contains
from discord.ext import commands

from cogs.base_cog import BaseCog
from spotify.spotify import Spotify

class Basic(BaseCog):
    def __init__(self, bot) -> None:
        super().__init__(bot)

    @commands.command()
    async def ping(self, ctx):
        if not ctx.channel.guild.me.guild_permissions.send_messages:
            return
        message = f'Pong! {round(self.bot.latency*1000)} ms'
        await ctx.send(message)
        return message

    @commands.command()
    async def play(self, ctx, arg):
        if (contains(arg, 'https://open.spotify.com/track/')):
            try:
                await ctx.send(Spotify.get_track(arg))
            except: # hibakezelés
                await ctx.send()

def setup(client):
    client.add_cog(Basic(client))