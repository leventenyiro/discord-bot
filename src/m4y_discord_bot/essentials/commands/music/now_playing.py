from essentials.commands.base_command import BaseCommand
from utils.logger import Logger
from utils.embeds import InfoEmbed, NowPlayingEmbed

class NowPlayingCommand(BaseCommand):
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
            (self.server and self.server['audio_player'].get_playlist_length() > 0, InfoEmbed('There is no song currently playing!')),
            (text_channel is not None and ctx.channel.id == text_channel.id, InfoEmbed(f'Commands can be accessed from {text_channel.name if text_channel is not None else None}!')) 
        ]
        response = [
            NowPlayingEmbed(self.server['audio_player'].get_current_song() if self.server else None) 
        ]
        super().__init__(ctx, required_permissions, response)

    async def logic(self, logging=True):
        pass
