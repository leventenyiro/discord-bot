import youtube_dl

class Song:
    YDL_OPTIONS = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }]
    }
    def __init__(self, url) -> None:
        self._url = url
        self.set_song_attributes(self.YDL_OPTIONS)

    def get_url(self):
        return self._url

    def set_song_attributes(self, options):
        with youtube_dl.YoutubeDL(options) as ydl:
            info = ydl.extract_info(self.get_url(), download=False)
            format = info['formats'][0]
            self.stream_url = format.get('url', None)
            self.title = info.get('title', None)
            self.duration_seconds = info.get('duration', 0)

    def get_stream_url(self):
            return self.stream_url
