import requests
from urllib.parse import urlparse
import json
from base64 import b64encode

class Spotify:
    def __init__(self, url):

        # Get bearer token

        file = open("./botconfig.json", "r")
        botinfo = json.loads(file.read())
        
        user_pass = b64encode(bytes(f'{botinfo["spotify_client_id"]}:{botinfo["spotify_client_secret"]}', encoding='utf8')).decode("ascii")

        response_auth = requests.post('https://accounts.spotify.com/api/token', headers={'Authorization': f'Basic {user_pass}'}, data={'grant_type': 'client_credentials'})

        # Get track

        track_id = urlparse(url).path.split('/')[2]
        endpoint = f'https://api.spotify.com/v1/tracks/{track_id}'
        headers = {'Authorization': f'Bearer {response_auth.json()["access_token"]}'}
        self.response = requests.get(endpoint, headers=headers)

    def get_track(self):
        track = self.response.json()
        try:
            return track["artists"][0]["name"] + " - " + track["name"]
        except:
            return "Error"