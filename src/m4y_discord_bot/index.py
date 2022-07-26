# pylint: skip-file

import discord
from discord.ext import commands
import json
import os
from utils.logger import Logger

os.system('')

# Loading botconfig
# FOR TESTING:
# botconfig has two attributes atm:
#   - token
#   - prefix as '-'
intents = discord.Intents.default()
intents.members = True
intents.messages = True
intents.voice_states = True
intents.reactions = True

prefix = os.environ.get('PREFIX')
bot = commands.Bot(command_prefix=prefix, intents=intents)

@bot.event
async def on_ready():
    Logger.success("The bot is online!")
    Logger.info(f"Currently online on {len(list(bot.guilds))} servers!")

# Loading command Cogs
for filename in os.listdir('./extensions'):
    if filename.endswith('.py') and not filename.startswith('base_') and filename != '__init__.py':
        Logger.progress(f'Loading {filename}...')
        bot.load_extension(f'extensions.{filename[:-3]}')

token = os.environ.get('TOKEN')
bot.run(token)