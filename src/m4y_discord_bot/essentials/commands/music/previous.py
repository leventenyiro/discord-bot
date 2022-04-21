from essentials.commands.base_command import BaseCommand
from utils.logger import Logger
from utils.embeds import InfoEmbed, PlayEmbed

class PreviousCommand(BaseCommand):
    def __init__(self, ctx, music_bot) -> None:
        self.music_bot = music_bot
        self.server = music_bot.get_server(ctx.channel.guild.id)
        previous_song = None
        if self.server:
            previous_song = self.server['audio_player'].get_previous_song()
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
            (ctx.author.voice is not None, InfoEmbed('You have to be in a voice channel to play the previous song!')),
            (self.server and self.server['audio_player'].get_previous_songs_length() > 0, InfoEmbed('There are no songs that have been played before!')),
            (text_channel is not None and ctx.channel.id == text_channel.id, InfoEmbed(f'Commands can be accessed from {text_channel.name if text_channel is not None else None}!')),
            (ctx.author.voice is not None and voice_channel is not None and ctx.author.voice.channel.id == voice_channel.id, InfoEmbed('We are not in the same room!'))
        ]
        response = [
            PlayEmbed(previous_song) if previous_song else None
        ]
        super().__init__(ctx, required_permissions, response)

    async def logic(self, logging=True):
        if logging:
            Logger.info(f'Playing the previous song on {self.ctx.guild.id}')
        audio_player = self.server['audio_player']
        audio_player.previous()
