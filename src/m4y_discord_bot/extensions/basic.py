from operator import contains
from discord.ext import commands

from extensions.base_cog import BaseCog
from external.spotify.spotify import Spotify

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

def setup(client):
    client.add_cog(Basic(client))