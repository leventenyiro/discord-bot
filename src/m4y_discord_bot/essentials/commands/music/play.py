import re
from external.spotify.spotify import Spotify
from external.youtube.youtube import Youtube
from essentials.commands.base_command import BaseCommand
from essentials.music.song import Song
from utils.logger import Logger
from utils.promptcolor import PromptColors
from utils.embeds import PlayEmbed, InfoEmbed

class PlayCommand(BaseCommand):
    def __init__(self, ctx, music_bot, url, *args, **kw) -> None:
        self.music_bot = music_bot
        self.ctx = ctx
        #self.song = self.create_song(url)
        self.song = kw.get('song', self.create_song(url, *args))
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
            (self.song and not self.song.failed, InfoEmbed('The song was not found!')),
            (text_channel is not None and ctx.channel.id == text_channel.id, InfoEmbed(f'Commands can be accessed from {text_channel.name if text_channel is not None else None}!')),
            (ctx.author.voice is not None and voice_channel is not None and ctx.author.voice.channel.id == voice_channel.id, InfoEmbed('We are not in the same room!'))
        ]
        response = [
            PlayEmbed(self.song) if self.song and not self.song.failed else None
        ]
        super().__init__(ctx, required_permissions, response)

    async def logic(self, logging=True):
        if logging:
            Logger.info(f'Request on {self.ctx.guild.id}.')
        server = self.music_bot.get_server(self.ctx.channel.guild.id)
        player = server['audio_player']
        if player.get_playlist_length() == 0:
            player.add_to_playlist(self.song)
            player.play(logging=logging)
        else:
            player.add_to_playlist(self.song)
    
    def create_song(self, url, *args):
        if url is None:
            return
        vid_id = None
        if url.startswith('https://open.spotify.com/'):
            try:
                if '/track/' in url:
                    url = Youtube.searchSong(Spotify.get_track(url))
                    pass
                elif '/playlist/' in url:
                    #Spotify.get_playlist(url) - returns list of author and title
                    pass
                elif '/album/' in url:
                    #Spotify.get_album(url) - returns list of author and title
                    pass
                else:
                    pass
            except Exception as ex:
                #print(ex) - Invalid link
                pass
        if url.startswith('https://www.youtube.com/watch?v='):
            vid_id = url.split('v=')[1][0:11]
        if url.startswith('https://youtu.be/'):
            vid_id = url.split('youtu.be/')[1][0:11]
        if vid_id is not None and re.match(r'^[a-zA-Z0-9_-]{11}$',vid_id) or re.match(r'^https:\/\/soundcloud\.com\/\S+$', url):
            Logger.info(f'A song has been created.')
            return Song(url, self.ctx)
        elif vid_id is None and url is not None:
            string = f"{url} {' '.join(f'{arg}' for arg in args)}"
            return self.create_song(Youtube.searchSong(string))
        return False
