import discord
import asyncio
import random
import math

from utils.logger import Logger

class AudioPlayer:
    # THESE CAN BE MODIFIED LATER, AND ALSO WE CAN ADD MORE FILTERS TO CREATE OTHER COMMANDS SUCH AS NIGHTCORE
    SPEED = 1.0
    SAMPLE_RATE = 48000
    MAX_PREVIOUS_SONG_COUNT = 50
    DEFAULT_SAMPLE_RATE = 48000
    NIGHTCORE_SAMPLE_RATE = 36000
    DAYCORE_SAMPLE_RATE = 64000
    QUEUE_RANGE = 5
    BASSBOOST_FREQUENCY = 120
    GAIN = 20
    # KNOWN BUGS:
    # - WHEN JOINING THE CHANNEL AFTER INITIALIZATION OF THE AUDIOPLAYER, YOU CANT HEAR THE BOT
    def __init__(self, voice_client) -> None:
        self.playlist = []
        self.previous_songs = []
        self.voice_client = voice_client
        self._loop = False
        self._nightcore = False
        self._daycore = False
        self._shuffle = False
        self._current_song_index = 0
        self._page = 0
        self._bassboost = False

    def get_playlist_length(self):
        return len(self.playlist)

    def get_previous_songs_length(self):
        return len(self.previous_songs)

    def get_previous_song(self):
        try:
            return self.previous_songs[-1]
        except IndexError:
            return None
    
    def get_current_song(self):
        try:
            return self.playlist[self._current_song_index]
        except IndexError:
            return None

    def play(self, logging=True):
        self._page = 0
        if self._shuffle:
            self._current_song_index = random.randint(0, self.get_playlist_length() - 1)
        else:
            self._current_song_index = 0
        current_song = self.get_current_song()
        stream_url = current_song.get_stream_url()
        stream = discord.FFmpegPCMAudio(stream_url, **self.GET_FFMPEG_OPTIONS())
        self.voice_client.play(stream, after=self._end_stream)
        if logging:
            Logger.info(f'({self.voice_client.guild.id}) Currently playing: {current_song.get_url()}.')

    def GET_FFMPEG_OPTIONS(self):
        FFMPEG_OPTIONS = {
            'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 60', 
            'options': f'-filter:a loudnorm,atempo={self.SPEED}{self._bassboost_options()} -vn -ar {self.SAMPLE_RATE}'
        }
        return FFMPEG_OPTIONS

    def _end_stream(self, error=None):
        if error:
            print(error)
        if not self.voice_client.is_connected():
            return
        if not self._loop:
            previous_song = self.playlist.pop(self._current_song_index)
            if previous_song is not None:
                self.previous_songs.append(previous_song)
            if self.get_previous_songs_length() > self.MAX_PREVIOUS_SONG_COUNT:
                self.previous_songs.pop(0)
        if self.get_playlist_length() > 0:
            self.play()
    
    def previous(self):
        previous_song = self.previous_songs.pop()
        self.playlist.insert(0,previous_song)
        if self.voice_client.is_playing():
            self.playlist.insert(0,None)
            return self.skip()
        self.play()

    def add_to_playlist(self, song):
        self.playlist.append(song)

    def remove_from_playlist(self, index):
        if self._shuffle and index - 1 < self._current_song_index:
            self._current_song_index -= 1
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
        self._daycore = False
        self._nightcore = not self._nightcore
        if self._nightcore:
            self.SAMPLE_RATE = self.NIGHTCORE_SAMPLE_RATE
        if not self._nightcore:
            self.SAMPLE_RATE = self.DEFAULT_SAMPLE_RATE

    def toggle_daycore(self):
        self._nightcore = False
        self._daycore = not self._daycore
        if self._daycore:
            self.SAMPLE_RATE = self.DAYCORE_SAMPLE_RATE
        if not self._daycore:
            self.SAMPLE_RATE = self.DEFAULT_SAMPLE_RATE

    def _bassboost_options(self):
        if self._bassboost:
            return f',equalizer=f=1:width_type=h:width={self.BASSBOOST_FREQUENCY}:g={self.GAIN}'
        return ''

    def toggle_bassboost(self):
        self._bassboost = not self._bassboost

    def is_daycore_mode(self):
        return self._daycore

    def is_nightcore_mode(self):
        return self._nightcore

    def is_bassboost_mode(self):
        return self._bassboost

    def set_speed(self, speed):
        self.SPEED = speed

    def toggle_shuffle(self):
        self._shuffle = not self._shuffle

    def is_shuffle(self):
        return self._shuffle

    def get_current_song_index(self):
        return self._current_song_index

    def get_page(self):
        return self._page

    def get_queue(self):
        queue = []
        for x in range(self._page*self.QUEUE_RANGE, self._page*self.QUEUE_RANGE+self.QUEUE_RANGE):
            try:
                queue.append((x,self.playlist[x]))
            except IndexError:
                pass
        return queue

    def get_max_page(self):
        return math.ceil(self.get_playlist_length()/self.QUEUE_RANGE)

    def increment_page(self):
        if self._page + 1 == self.get_max_page():
            return
        self._page += 1

    def decrement_page(self):
        if self._page - 1 == -1:
            return
        self._page -= 1
