import discord
from discord.ext import commands
from cogs.base_cog import BaseCog

class Basic(BaseCog):
    def __init__(self, bot) -> None:
        super().__init__(bot)

    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f'Pong! {round(self.bot.latency*1000)} ms')

def setup(client):
    client.add_cog(Basic(client))