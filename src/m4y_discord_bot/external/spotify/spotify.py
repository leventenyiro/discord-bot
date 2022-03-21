import requests
import json
from urllib.parse import urlparse
from base64 import b64encode

class Spotify:
    @staticmethod
    def get_track(url):
        file = open("./botconfig.json", "r")
        botinfo = json.loads(file.read())
        user_pass = b64encode(bytes(f'{botinfo["spotify_client_id"]}:{botinfo["spotify_client_secret"]}', encoding='utf8')).decode("ascii")
        response_auth = requests.post('https://accounts.spotify.com/api/token', headers={'Authorization': f'Basic {user_pass}'}, data={'grant_type': 'client_credentials'})

        track_id = urlparse(url).path.split('/track/')[1]
        endpoint = f'https://api.spotify.com/v1/tracks/{track_id}'
        headers = {'Authorization': f'Bearer {response_auth.json()["access_token"]}'}
        response = requests.get(endpoint, headers=headers)

        track = response.json()
        try:
            return track["artists"][0]["name"] + " - " + track["name"]
        except:
            raise Exception("Invalid link")
