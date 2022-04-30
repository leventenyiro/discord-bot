import unittest
from urllib import response
from external.spotify.spotify import Spotify
from utility.mockups import *

class TestSpotifyApi(unittest.TestCase):
    def setUp(self):
        self.url = None
        self.spotifyapi = unittest.mock.MagicMock()
        title = unittest.mock.MagicMock()
        self.spotifyapi.get_track.return_value = title

    def test_spotify_api_basic(self):
        Spotify.get_track(self.url)
        self.spotifyapi.assert_called()
