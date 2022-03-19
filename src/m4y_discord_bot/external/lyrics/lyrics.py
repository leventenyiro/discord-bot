import json
import re
import lyricsgenius

class Lyrics:
    @staticmethod
    def get_lyrics(song_title):
        file = open("./botconfig.json", "r")
        botinfo = json.loads(file.read())
        
        genius = lyricsgenius.Genius(botinfo["genius_access_token"])
        lyricsgenius.PublicAPI()
        lyrics = re.sub(r'[0-9]*Embed$', '', genius.search_song(song_title).lyrics)
        return lyrics