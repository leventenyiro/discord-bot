import math
import datetime
import re

from discord import Embed
from discord import Colour

BOTNAME = "Music4You"
PFP_LINK = "https://cdn.discordapp.com/avatars/940645443359092806/12cbd729c419913c0bf3373173ac7c01.png"
COLOR = Colour.from_rgb(34,139,34)
SOUNDCLOUD_EMOTE = '<:soundcloud:966757896417329173>'
YOUTUBE_EMOTE = '<:youtube:966757552765403196>'

class BaseEmbed(Embed):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.color = COLOR
        self.set_author(name=BOTNAME, icon_url=PFP_LINK)

class MusicEmbed(BaseEmbed):
    def __init__(self, song, title,**kwargs):
        super().__init__(**kwargs)
        if song is None:
            return
        self.url = song.get_url()
        if self.url.startswith('https://youtu.be/') or self.url.startswith('https://www.youtube.com/watch?v='):
            self.icon = YOUTUBE_EMOTE
        if re.match(r'^https:\/\/soundcloud\.com\/\S+$', self.url):
            self.icon = SOUNDCLOUD_EMOTE
        self.title = f'{self.icon} {title}'
        self.description = f'{song.title}'
        self.set_footer(text=f'Requested by: {song.requested_by}', icon_url=song.requested_by_pfp)
        self.set_thumbnail(url=song.thumbnail)

class InfoEmbed(BaseEmbed):
    def __init__(self, message):
        super().__init__()
        self.title = message

class NowPlayingEmbed(MusicEmbed):
    BAR_LENGTH = 50
    def __init__(self, song):
        super().__init__(song, 'Now Playing')
        if song is not None and not song.is_live:
            self.add_field(name=self._generate_time_bar(song), value=f'{self._time_conversion(self._get_current_duration(song))}/{self._time_conversion(song.duration_seconds)}')

    def _generate_time_bar(self, song):
        diff = self._get_current_duration(song)
        percentage = diff/song.duration_seconds
        bar = ''
        for x in range(0, self.BAR_LENGTH):
            if x == math.floor(percentage*self.BAR_LENGTH):
                bar += '⬤'
            else:
                bar += '-'
        return bar
    
    def _get_current_duration(self, song):
        current_timestamp = math.floor(datetime.datetime.now().timestamp())
        diff = current_timestamp-song.started_timestamp_seconds
        return diff

    def _time_conversion(self, time):
        minutes = math.floor(time / 60)
        minute_string = ''
        if minutes < 10:
            minute_string = f'0{minutes}'
        else:
            minute_string = f'{minutes}'
        seconds = time % 60
        second_string = ''
        if seconds < 10:
            second_string = f'0{seconds}'
        else:
            second_string = f'{seconds}'
        return f'{minute_string}:{second_string}'

class PlayEmbed(MusicEmbed):
    def __init__(self, song):
        super().__init__(song, 'Added Song')

class QueueEmbed(BaseEmbed):
    def __init__(self, audio_player, **kwargs):
        super().__init__(**kwargs)
        if audio_player is None:
            return
        self._queue = audio_player.get_queue()
        self._page = audio_player.get_page()+1
        self._max_page = audio_player.get_max_page()
        self.title = 'The current queue'
        self.description = self._get_queue_values()
        self.set_footer(text=f'{self._page}/{self._max_page}')

    def _get_queue_values(self):
        value = ""
        for song in self._queue:
            index = song[0]
            song_obj = song[1]
            value += f'`{index+1}.` [{song_obj.title}]({song_obj.get_url()}) | `{self._time_conversion(song_obj.duration_seconds)} Requested by: {song_obj.requested_by}`\n'
        return value

    def _time_conversion(self, time):
        minutes = math.floor(time / 60)
        minute_string = ''
        if minutes < 10:
            minute_string = f'0{minutes}'
        else:
            minute_string = f'{minutes}'
        seconds = time % 60
        second_string = ''
        if seconds < 10:
            second_string = f'0{seconds}'
        else:
            second_string = f'{seconds}'
        return f'{minute_string}:{second_string}'
