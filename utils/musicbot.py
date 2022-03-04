import asyncio
import discord
from utils.logger import Logger
from utils.promptcolor import PromptColors

class MusicBot:
    def __init__(self, bot) -> None:
        self.bot = bot
        self.servers = {}

    async def connect(self, ctx):
        # checks if the bot is already in a voice channel on the server or not
        try:
            server = self.servers[ctx.guild.id]
            return await ctx.send('Már bent vagyok egy szobában!')
        except KeyError:
            pass
        # checks whether the user is on a voice channel or not
        if not ctx.author.voice.channel:
            return await ctx.send('Voice channelben kell lenned, hogy tudjak hozzád csatlakozni!')
        # checks for speak permission for the voice channel
        if not ctx.channel.guild.me.guild_permissions.speak:
            return await ctx.send('Nincs jogom a beszédhez a szobában!')
        # checks for connect permission for the voice channel
        if not ctx.channel.guild.me.guild_permissions.connect:
            return await ctx.send('Nincs jogom csatlakozni a szobához!')
        # check if there is room for the bot to join
        if ctx.author.voice.channel.user_limit == len(ctx.author.voice.channel.members):
            return await ctx.send('A szoba tele van!')
        voice_channel = ctx.author.voice.channel
        text_channel = ctx.channel
        self.servers[ctx.channel.guild.id] = {
            'voice_channel': voice_channel, 
            'message_channel': text_channel
        }
        Logger.info(f'Joined to {PromptColors.CGREENBG}{voice_channel.id}{PromptColors.CEND} voice channel on {PromptColors.CGREENBG}{ctx.channel.guild.id}{PromptColors.CEND} guild, using {PromptColors.CGREENBG}{text_channel.id}{PromptColors.CEND} text channel!')
        await text_channel.send(f'Csatlakoztam a {voice_channel.name} szobába!')
        await text_channel.send(f'A parancsok mostantól a {text_channel.name} szobában érhetőek el!')
        try:
            return await voice_channel.connect()
        except asyncio.TimeoutError:
            Logger.error(f'ERROR: Timeout while trying to join to {PromptColors.CGREENBG}{voice_channel.id}{PromptColors.CEND} voice channel on {PromptColors.CGREENBG}{ctx.channel.guild.id}{PromptColors.CEND} guild')
            return await text_channel.send(f'A csatlakozás sikertelen volt!')
    
    async def disconnect(self, ctx):
        # TO DO:
        # DELETING TEXT CHANNEL WHILE THE BOT IS ONLINE

        # checks if the bot is in a voice channel on the server or not
        try:
            server = self.servers[ctx.guild.id]
        except KeyError:
            return await ctx.send('Nem vagyok fent egy szobában sem!')
        # checks whether the user is on a voice channel or not
        if not ctx.author.voice.channel:
            return await ctx.send('Voice channelben kell lenned, hogy le tudj csatlakoztatni!')
        # checks if the command has been called from the same text channel, which it has been initialized
        # if the text channel is none ()
        text_channel = server['message_channel']
        if text_channel is not None and ctx.channel.id != text_channel.id:
            return await ctx.channel.send(f'A parancsok a {text_channel.name} szobában érhetőek el!')
        # checks if the user is in the same channel or not
        voice_channel = server['voice_channel']
        if ctx.author.voice.channel.id != voice_channel.id:
            return await ctx.send('Nem vagyunk ugyanabban a szobában!')
        await ctx.voice_client.disconnect()
        Logger.info(f'Disconnected from {PromptColors.CGREENBG}{voice_channel.id}{PromptColors.CEND} voice channel on {PromptColors.CGREENBG}{ctx.channel.guild.id}{PromptColors.CEND} guild')
        self.clear_server(ctx.guild.id)
        return await text_channel.send(f'Lecsatlakozva!')
    
    def clear_server(self, id):
        del self.servers[id]

    def update_voice_channel(self, id, channel):
        self.servers[id]['voice_channel'] = channel

    def get_server(self, id):
        try:
            return self.servers[id]
        except KeyError:
            return False
