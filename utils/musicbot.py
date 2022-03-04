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
        return await voice_channel.connect()