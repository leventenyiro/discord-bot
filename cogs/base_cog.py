import discord
from discord.ext import commands
from utils.logger import Logger
from utils.promptcolor import PromptColors

class BaseCog(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        Logger.success(f'The bot has loaded the {PromptColors.CGREENBG}{PromptColors.CWHITE}{self.__class__.__name__}{PromptColors.CEND}{PromptColors.CGREEN} command Cog!')

