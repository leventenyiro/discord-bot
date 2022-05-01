import unittest

from external.spotify.spotify import Spotify
from utility.mockups import *

class TestSpotifyApi(unittest.TestCase):
    def setUp(self):
        self.spotifyapi = unittest.mock.MagicMock()
        title = unittest.mock.MagicMock()
        self.request = unittest.mock.MagicMock()
        self.request.post.return_value = title
        self.kwargs = { 'spotify': self.spotifyapi }

    def test_spotify_api_get_track(self):
        Spotify.get_track("/track/", **self.kwargs)
        self.spotifyapi.post.assert_called()
        self.spotifyapi.get.assert_called()

    def test_spotify_api_get_playlist(self):
        Spotify.get_playlist("/playlist/", **self.kwargs)
        self.spotifyapi.post.assert_called()
        self.spotifyapi.get.assert_called()

    def test_spotify_api_get_album(self):
        Spotify.get_album("/album/", **self.kwargs)
        self.spotifyapi.post.assert_called()
        self.spotifyapi.get.assert_called()
