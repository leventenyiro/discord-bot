import discord
from discord.ext import commands
import json
import os

# Loading botconfig
# FOR TESTING:
# botconfig has two attributes atm:
#   - token
#   - prefix as '-'
file = open("./botconfig.json", "r")
botinfo = json.loads(file.read())

prefix = botinfo["prefix"]
bot = commands.Bot(command_prefix=prefix)

# Loading command Cogs
for filename in os.listdir('./cogs'):
    if filename.endswith('.py') and not filename.startswith('base_'):
        print(f'Loading {filename}...')
        bot.load_extension(f'cogs.{filename[:-3]}')

token = botinfo["token"]
bot.run(token)