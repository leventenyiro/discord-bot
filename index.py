from sys import prefix
import discord
from discord.ext import commands
import json


file = open("./botconfig.json", "r")
botinfo = json.loads(file.read())

prefix = botinfo["prefix"]
bot = commands.Bot(command_prefix=prefix)

token = botinfo["token"]
bot.run(token)