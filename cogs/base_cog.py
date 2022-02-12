import discord
from discord.ext import commands

class BaseCog(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'The bot has loaded the {self.__class__.__name__} command Cog!')

