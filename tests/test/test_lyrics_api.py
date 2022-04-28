import unittest
from urllib import response
from external.lyrics.lyrics import Lyrics
# from essentials.music.audioplayer import AudioPlayer
# from essentials.music.musicbot import MusicBot
from utility.mockups import *
# az a lényeg, hogy a search_song lefusson

class TestLyricsApi(unittest.TestCase):
    def setUp(self):
        self.song_title = None
        self.lyricsapi = unittest.mock.MagicMock()
        lyrics = unittest.mock.MagicMock()
        self.lyrics_genius = unittest.mock.MagicMock()
        lyrics.full_title = "valami"
        lyrics.url = "valami"
        self.lyrics_genius.search_song.return_value = lyrics
        self.kwargs = { 'lyrics': self.lyricsapi, 'lyrics_genius': self.lyrics_genius }

    def test_lyrics_api_basic(self):
        Lyrics.get_lyrics(self.song_title, **self.kwargs)
        self.lyrics_genius.search_song.assert_called()
