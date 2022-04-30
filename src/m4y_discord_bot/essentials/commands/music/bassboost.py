from essentials.commands.base_command import BaseCommand
from utils.logger import Logger
from utils.embeds import InfoEmbed

class BassboostCommand(BaseCommand):
    def __init__(self, ctx, music_bot) -> None:
        self.music_bot = music_bot
        self.server = music_bot.get_server(ctx.channel.guild.id)
        try:
            text_channel = self.server['text_channel']
        except Exception:
            text_channel = None
        try:
            voice_channel = self.server['voice_channel']
        except Exception:
            voice_channel = None
        required_permissions = [
            (self.server, InfoEmbed('I am not on any voice channel!')),
            (ctx.author.voice is not None, InfoEmbed('You have to be in a voice channel to toggle the bassboost mode!')),
            (text_channel is not None and ctx.channel.id == text_channel.id, InfoEmbed(f'Commands can be accessed from {text_channel.name if text_channel is not None else None}!')), 
            (ctx.author.voice is not None and voice_channel is not None and ctx.author.voice.channel.id == voice_channel.id, InfoEmbed('We are not in the same room!'))
        ]
        response = [
            InfoEmbed(f'Bassboost mode is {"off" if self.server and self.server["audio_player"].is_bassboost_mode() else "on"}!') 
        ]
        super().__init__(ctx, required_permissions, response)

    async def logic(self, logging=True):
        audioplayer = self.server['audio_player']
        audioplayer.toggle_bassboost()
        if logging:
            Logger.info(f'Bassboost mode is {"on" if self.server and self.server["audio_player"].is_bassboost_mode() else "off"} on {self.ctx.channel.guild.id}!')
