import math
import datetime

from discord import Embed
from discord import Colour

botname = "Music4You"
pfp_link = "https://cdn.discordapp.com/avatars/940645443359092806/12cbd729c419913c0bf3373173ac7c01.png"
color = Colour.from_rgb(34,139,34)

class InfoEmbed(Embed):
    def __init__(self, message):
        super().__init__()
        self.color = color
        self.title = message
        self.set_author(name=botname, icon_url=pfp_link)

class NowPlayingEmbed(Embed):
    BAR_LENGTH = 50
    def __init__(self, song):
        super().__init__()
        if song is None:
            return
        self.color = color
        self.title = 'Now playing'
        self.url = song.get_url()
        self.description = f'{song.title}'
        if not song.is_live:
            self.add_field(name=self._generate_time_bar(song), value=f'{self._time_conversion(self._get_current_duration(song))}/{self._time_conversion(song.duration_seconds)}')
        self.set_footer(text=f'Requested by: {song.requested_by}', icon_url=song.requested_by_pfp)
        self.set_author(name=botname, icon_url=pfp_link)
        self.set_thumbnail(url=song.thumbnail)

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
