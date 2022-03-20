import re
from src.m4y_discord_bot.external.spotify import Spotify
from essentials.commands.base_command import BaseCommand
from essentials.music.song import Song
from utils.logger import Logger
from utils.promptcolor import PromptColors
from utils.embeds import InfoEmbed

class PlayCommand(BaseCommand):
    def __init__(self, ctx, music_bot, url) -> None:
        self.music_bot = music_bot
        self.song = self.create_song(url)
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
            (ctx.author.voice is not None, InfoEmbed('You have to be in a voice channel to play a song!')),
            (self.song, InfoEmbed('The requested song is not in the correct format!')),
            (text_channel is not None and ctx.channel.id == text_channel.id, InfoEmbed(f'Commands can be accessed from {text_channel.name if text_channel is not None else None}!')),
            (ctx.author.voice is not None and voice_channel is not None and ctx.author.voice.channel.id == voice_channel.id, InfoEmbed('We are not in the same room!'))
        ]
        response = [
            InfoEmbed('A new song has been added to the playlist!')
        ]
        super().__init__(ctx, required_permissions, response)

    async def logic(self, logging=True):
        Logger.info(f'Request on {self.ctx.guild.id}.')
        server = self.music_bot.get_server(self.ctx.channel.guild.id)
        player = server['audio_player']
        if player.get_playlist_length() == 0:
            player.add_to_playlist(self.song)
            await player.play()
        else:
            player.add_to_playlist(self.song)
    
    def create_song(self, url):
        vid_id = None
        if url.startswith('https://www.youtube.com/watch?v='):
            vid_id = url.split('v=')[1][0:11]
        if url.startswith('https://youtu.be/'):
            vid_id = url.split('youtu.be/')[1][0:11]
        if url.startswith('https://open.spotify.com/') and r'^(track\/)(.*))':
            pass
        if vid_id is not None and re.match(r'^[a-zA-Z0-9_-]{11}$',vid_id):
            Logger.info(f'A song has been created.')
            return Song(url)
        return False