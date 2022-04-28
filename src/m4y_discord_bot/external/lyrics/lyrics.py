import json
import lyricsgenius

class Lyrics:
    @staticmethod
    def get_lyrics(song_title, **kw):
        lyrics_object = kw.get('lyrics', lyricsgenius)
        
        try:
            file = open("./botconfig.json", "r")
            botinfo = json.loads(file.read())
            lyrics_genius = lyrics_object.Genius(botinfo["genius_access_token"])
        except:
            lyrics_genius = kw.get('lyrics_genius', None)
            pass
        lyrics_data = lyrics_genius.search_song(song_title)
        lyrics = {'full_title': lyrics_data.full_title, 'url': lyrics_data.url}
        return lyrics
