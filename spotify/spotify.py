import requests
from urllib.parse import urlparse
import secrets as secrets

class Spotify:
    def __init__(self, url):
        track_id = urlparse(url).path.split('/')[2]

        endpoint = f'https://api.spotify.com/v1/tracks/{track_id}'
        headers = {'Authorization': f'Bearer {secrets.spotify_token}'}
        self.response = requests.get(endpoint, headers=headers)

    def getTrack(self):
        track = self.response.json()
        return track["artists"][0]["name"] + " - " + track["name"]