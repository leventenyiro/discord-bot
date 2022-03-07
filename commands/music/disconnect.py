from commands.base_command import BaseCommand
from utils.logger import Logger
from utils.promptcolor import PromptColors

class DisconnectCommand(BaseCommand):
    def __init__(self, ctx, music_bot) -> None:
        server = music_bot.get_server(ctx.channel.guild.id)
        try:
            text_channel = server['text_channel']
        except Exception:
            text_channel = None
        try:
            voice_channel = server['voice_channel']
        except Exception:
            voice_channel = None
        required_permissions = [
            (server, 'Nem vagyok fent egy szobában sem!'),
            (ctx.author.voice is not None, 'Voice channelben kell lenned, hogy le tudj csatlakoztatni!'),
            (text_channel is not None and ctx.channel.id == text_channel.id, f'A parancsok a {text_channel.name if text_channel is not None else None} szobában érhetőek el!'),
            (ctx.author.voice is not None and voice_channel is not None and ctx.author.voice.channel.id == voice_channel.id, 'Nem vagyunk ugyanabban a szobában!')
        ]
        response = [
            'Lecsatlakozva!'
        ]
        super().__init__(ctx, required_permissions, response)
        self.music_bot = music_bot

    async def logic(self):
        server = self.music_bot.get_server(self.ctx.channel.guild.id)
        voice_channel = server['voice_channel']
        await self.ctx.voice_client.disconnect()
        Logger.info(f'Disconnected from {PromptColors.CGREENBG}{voice_channel.id}{PromptColors.CEND} voice channel on {PromptColors.CGREENBG}{self.ctx.channel.guild.id}{PromptColors.CEND} guild')
        self.music_bot.clear_server(self.ctx.guild.id)

