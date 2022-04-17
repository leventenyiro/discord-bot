import discord
import asyncio

from utils.logger import Logger

class AudioPlayer:
    # THESE CAN BE MODIFIED LATER, AND ALSO WE CAN ADD MORE FILTERS TO CREATE OTHER COMMANDS SUCH AS NIGHTCORE
    SPEED = 1.0
    SAMPLE_RATE = 48000

    DEFAULT_SAMPLE_RATE = 48000
    NIGHTCORE_SAMPLE_RATE = 36000
    # KNOWN BUGS:
    # - WHEN JOINING THE CHANNEL AFTER INITIALIZATION OF THE AUDIOPLAYER, YOU CANT HEAR THE BOT
    def __init__(self, voice_client) -> None:
        self.playlist = []
        self.voice_client = voice_client
        self._loop = False
        self._nightcore = False

    def get_playlist_length(self):
        return len(self.playlist)

    def get_current_song(self):
        try:
            return self.playlist[0]
        except IndexError:
            return None

    async def play(self, logging=True):
        current_song = self.get_current_song()
        stream_url = current_song.get_stream_url()
        stream = discord.FFmpegPCMAudio(stream_url, **self.GET_FFMPEG_OPTIONS())
        self.voice_client.play(stream, after=self._end_stream)
        if logging:
            Logger.info(f'({self.voice_client.guild.id}) Currently playing: {current_song.get_url()}.')

    def GET_FFMPEG_OPTIONS(self):
        FFMPEG_OPTIONS = {
            'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 60', 
            'options': f'-filter_complex atempo={self.SPEED} -vn -ar {self.SAMPLE_RATE}'
        }
        return FFMPEG_OPTIONS

    def _end_stream(self, error=None):
        if error:
            print(error)
        if not self._loop:
            self.playlist.pop(0)
        if self.get_playlist_length() > 0:
            asyncio.run(self.play())

    def add_to_playlist(self, song):
        self.playlist.append(song)

    def remove_from_playlist(self, index):
        del self.playlist[index - 1]

    def skip(self):
        if self._loop:
            self._loop = False
        if self.voice_client.is_playing():
            self.voice_client.stop()
    
    def loop(self):
        self._loop = not self._loop

    def is_looped(self):
        return self._loop

    def pause(self):
        if self.is_paused():
            self.voice_client.resume()
            return
        self.voice_client.pause()

    def is_paused(self):
        return self.voice_client.is_paused()
    
    def toggle_nightcore(self):
        self._nightcore = not self._nightcore
        if self._nightcore:
            self.SAMPLE_RATE = self.NIGHTCORE_SAMPLE_RATE
        if not self._nightcore:
            self.SAMPLE_RATE = self.DEFAULT_SAMPLE_RATE

    def is_nightcore_mode(self):
        return self._nightcore
