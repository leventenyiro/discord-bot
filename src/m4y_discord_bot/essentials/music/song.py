import youtube_dl
import datetime
import math

class Song:
    YDL_OPTIONS = {
        'ignoreerrors': True,
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }]
    }
    def __init__(self, url, ctx) -> None:
        self._url = url
        self.requested_by = ctx.author.nick if ctx.author.nick is not None else ctx.author.name
        self.requested_by_pfp = f'https://cdn.discordapp.com/avatars/{ctx.author.id}/{ctx.author.avatar}'
        self.failed = True
        self.set_song_attributes(self.YDL_OPTIONS)

    def get_url(self):
        return self._url

    def set_song_attributes(self, options):
        with youtube_dl.YoutubeDL(options) as ydl:
            info = ydl.extract_info(self.get_url(), download=False)
            if info is not None:
                self.failed = False
                format = info['formats'][0]
                self.stream_url = format.get('url', None)
                self.title = info.get('title', None)
                self.duration_seconds = math.floor(info.get('duration', 0))
                self.thumbnail = info.get('thumbnail', None)
                self.is_live = info.get('is_live', None)
                self.started_timestamp_seconds = math.floor(datetime.datetime.now().timestamp())

    def get_stream_url(self):
        if hasattr(self, 'stream_url'):
            return self.stream_url
        return False
