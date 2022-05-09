import requests
import json
import os

from urllib.parse import urlparse
from base64 import b64encode

class Spotify:
    @staticmethod
    def get_track(url, **kw):
        spotify_object = kw.get('spotify', requests)
        user_pass = b64encode(bytes(f'{os.environ.get("SPOTIFY_CLIENT_ID")}:{os.environ.get("SPOTIFY_CLIENT_SECRET")}', encoding='utf8')).decode("ascii")

        response_auth = spotify_object.post('https://accounts.spotify.com/api/token', headers={'Authorization': f'Basic {user_pass}'}, data={'grant_type': 'client_credentials'})

        track_id = urlparse(url).path.split('/track/')[1]
        endpoint = f'https://api.spotify.com/v1/tracks/{track_id}'
        headers = {'Authorization': f'Bearer {response_auth.json()["access_token"]}'}
        response = spotify_object.get(endpoint, headers=headers)
        track = response.json()
        try:
            return track["artists"][0]["name"] + " - " + track["name"]
        except:
            raise Exception("Invalid link")

    @staticmethod
    def get_playlist(url, **kw):
        spotify_object = kw.get('spotify', requests)
        user_pass = b64encode(bytes(f'{os.environ.get("SPOTIFY_CLIENT_ID")}:{os.environ.get("SPOTIFY_CLIENT_SECRET")}', encoding='utf8')).decode("ascii")

        response_auth = spotify_object.post('https://accounts.spotify.com/api/token', headers={'Authorization': f'Basic {user_pass}'}, data={'grant_type': 'client_credentials'})
        
        playlist_id = urlparse(url).path.split('/playlist/')[1]
        endpoint = f'https://api.spotify.com/v1/playlists/{playlist_id}/tracks?fields=items(track(artists, name))'
        headers = {'Authorization': f'Bearer {response_auth.json()["access_token"]}'}
        response = spotify_object.get(endpoint, headers=headers)

        playlist = response.json()
        tracks = []
        try:
            for item in playlist["items"]:
                tracks.append(item["track"]["artists"][0]["name"] + " - " + item["track"]["name"])
            return tracks
        except:
            raise Exception("Invalid link")

    @staticmethod
    def get_album(url, **kw):
        spotify_object = kw.get('spotify', requests)
        user_pass = b64encode(bytes(f'{os.environ.get("SPOTIFY_CLIENT_ID")}:{os.environ.get("SPOTIFY_CLIENT_SECRET")}', encoding='utf8')).decode("ascii")

        response_auth = spotify_object.post('https://accounts.spotify.com/api/token', headers={'Authorization': f'Basic {user_pass}'}, data={'grant_type': 'client_credentials'})

        album_id = urlparse(url).path.split('/album/')[1]
        endpoint = f'https://api.spotify.com/v1/albums/{album_id}/tracks'
        headers = {'Authorization': f'Bearer {response_auth.json()["access_token"]}'}
        response = spotify_object.get(endpoint, headers=headers)

        album = response.json()
        tracks = []
        try:
            for item in album["items"]:
                tracks.append(item["artists"][0]["name"] + " - " + item["name"])
            return tracks
        except:
            raise Exception("Invalid link")
