import json
import lyricsgenius

class Lyrics:
    @staticmethod
    def get_lyrics(song_title):
        file = open("./botconfig.json", "r")
        botinfo = json.loads(file.read())
        
        try:
            genius = lyricsgenius.Genius(botinfo["genius_access_token"])
            lyrics = {'full_title': genius.search_song(song_title).full_title, 'url': genius.search_song(song_title).url}
        except:
            lyrics = {'full_title': None, 'url': None}
        return lyrics
