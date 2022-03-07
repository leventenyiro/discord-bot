import asyncio

from commands.base_command import BaseCommand
from utils.logger import Logger
from utils.promptcolor import PromptColors

class ConnectCommand(BaseCommand):
    def __init__(self, ctx, music_bot) -> None:
        required_permissions = [
            (not music_bot.get_server(ctx.channel.guild.id), 'Már bent vagyok egy szobában!'),
            (ctx.author.voice is not None, 'Voice channelben kell lenned, hogy tudjak hozzád csatlakozni!'),
            (ctx.channel.guild.me.guild_permissions.speak, 'Nincs jogom a beszédhez a szobában!'),
            (ctx.channel.guild.me.guild_permissions.connect, 'Nincs jogom csatlakozni a szobához!'),
            (ctx.author.voice is not None and ctx.author.voice.channel.user_limit < len(ctx.author.voice.channel.members), 'A szoba tele van!')
        ]
        response = [
            f'Csatlakoztam a {None if ctx.author.voice is None else ctx.author.voice.channel.name} szobába!',
            f'A parancsok mostantól a {ctx.channel.name} szobában érhetőek el!'
        ]
        super().__init__(ctx, required_permissions, response)
        self.music_bot = music_bot

    async def logic(self):
        voice_channel = self.ctx.author.voice.channel
        text_channel = self.ctx.channel
        server = {
            'voice_channel': voice_channel, 
            'text_channel': text_channel
        }
        self.music_bot.add_server(self.ctx.channel.guild.id, server)
        Logger.info(f'Joined to {PromptColors.CGREENBG}{voice_channel.id}{PromptColors.CEND} voice channel on {PromptColors.CGREENBG}{self.ctx.channel.guild.id}{PromptColors.CEND} guild, using {PromptColors.CGREENBG}{text_channel.id}{PromptColors.CEND} text channel!')
        try:
            return await voice_channel.connect()
        except asyncio.TimeoutError:
            Logger.error(f'ERROR: Timeout while trying to join to {PromptColors.CGREENBG}{voice_channel.id}{PromptColors.CEND} voice channel on {PromptColors.CGREENBG}{self.ctx.channel.guild.id}{PromptColors.CEND} guild')
            return await text_channel.send(f'A csatlakozás sikertelen volt!')
