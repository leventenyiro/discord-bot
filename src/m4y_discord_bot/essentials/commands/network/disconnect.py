from essentials.commands.base_command import BaseCommand
from utils.embeds import InfoEmbed
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
            (server, InfoEmbed('I am not on any voice channel!')),
            (ctx.author.voice is not None, InfoEmbed('You have to be in a voice channel to disconnect me!')),
            (text_channel is not None and ctx.channel.id == text_channel.id, InfoEmbed(f'Commands can be accessed from {text_channel.name if text_channel is not None else None}!')),
            (ctx.author.voice is not None and voice_channel is not None and ctx.author.voice.channel.id == voice_channel.id, InfoEmbed('We are not in the same room!'))
        ]
        response = [
            InfoEmbed('Disconnected!')
        ]
        super().__init__(ctx, required_permissions, response)
        self.music_bot = music_bot

    async def logic(self, logging=True):
        server = self.music_bot.get_server(self.ctx.channel.guild.id)
        voice_channel = server['voice_channel']
        await self.ctx.voice_client.disconnect()
        if logging:
            Logger.info(f'Disconnected from {PromptColors.CGREENBG}{voice_channel.id}{PromptColors.CEND} voice channel on {PromptColors.CGREENBG}{self.ctx.channel.guild.id}{PromptColors.CEND} guild')
        self.music_bot.clear_server(self.ctx.guild.id)
