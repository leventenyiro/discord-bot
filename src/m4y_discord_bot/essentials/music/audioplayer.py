import youtube_dl
import discord
import asyncio

from utils.logger import Logger

class AudioPlayer:
    # THESE CAN BE MODIFIED LATER, AND ALSO WE CAN ADD MORE FILTERS TO CREATE OTHER COMMANDS SUCH AS NIGHTCORE
    SPEED = 1.0
    SAMPLE_RATE = 48000
    # KNOWN BUGS:
    # - WHEN JOINING THE CHANNEL AFTER INITIALIZATION OF THE AUDIOPLAYER, YOU CANT HEAR THE BOT
    FFMPEG_OPTIONS = {
        'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 60', 
        'options': f'-filter_complex atempo={SPEED} -vn -ar {SAMPLE_RATE}'
    }
    YDL_OPTIONS = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }]
    }
    def __init__(self, voice_client) -> None:
        self.playlist = []
        self.voice_client = voice_client

    def get_playlist_length(self):
        return len(self.playlist)

    def get_current_song(self):
        return self.playlist[0]

    async def play(self):
        with youtube_dl.YoutubeDL(self.YDL_OPTIONS) as ydl:
            current_song = self.get_current_song()
            stream_url = current_song.get_stream(self.YDL_OPTIONS)
            stream = discord.FFmpegPCMAudio(stream_url, **self.FFMPEG_OPTIONS)
            self.voice_client.play(stream, after=self._end_stream)
            Logger.info(f'({self.voice_client.guild.id}) Currently playing: {current_song.get_url()}.')

    def _end_stream(self, error):
        if error:
            print(error)
        self.playlist.pop(0)
        if self.get_playlist_length() > 0:
            asyncio.run(self.play())

    def add_to_playlist(self, song):
        self.playlist.append(song)