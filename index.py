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

file = open("./botconfig.json", "r")
botinfo = json.loads(file.read())

prefix = botinfo["prefix"]
bot = commands.Bot(command_prefix=prefix, intents=intents)

@bot.event
async def on_ready():
    Logger.success("The bot is online!")
    Logger.info(f"Currently online on {len(list(bot.guilds))} servers!")

# Loading command Cogs
for filename in os.listdir('./cogs'):
    if filename.endswith('.py') and not filename.startswith('base_'):
        Logger.progress(f'Loading {filename}...')
        bot.load_extension(f'cogs.{filename[:-3]}')

token = botinfo["token"]
bot.run(token)