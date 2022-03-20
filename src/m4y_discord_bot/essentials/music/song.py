import youtube_dl

class Song:
    def __init__(self, url) -> None:
        self._url = url

    def get_url(self):
        return self._url

    def get_stream(self, options):
        with youtube_dl.YoutubeDL(options) as ydl:
            return ydl.extract_info(self.get_url(), download=False)['formats'][0]['url']
