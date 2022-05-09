import json
import lyricsgenius
import os

class Lyrics:
    @staticmethod
    def get_lyrics(song_title, **kw):
        lyrics_object = kw.get('lyrics', lyricsgenius)
        lyrics_genius = kw.get('lyrics_genius', lyrics_object.Genius(os.environ.get('GENIUS_ACCESS_TOKEN')))
        lyrics_data = lyrics_genius.search_song(song_title)
        try:
            return {'full_title': lyrics_data.full_title, 'url': lyrics_data.url}
        except:
            return {'full_title': None, 'url': None}
