# pylint: skip-file

import urllib.request
import re
import os

from urllib.parse import quote
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

class Youtube:
    @staticmethod
    def searchSong(message):
        data = message.split()
        if(len(data) > 1):
            data = "+".join(data)
        else:
            data = data[0]

        # encoding data
        data = quote(data)

        html = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + data)
        video_ids = re.findall("watch\?v=(\S{11})", html.read().decode())
        print("https://www.youtube.com/watch?v=" + video_ids[0])
        return "https://www.youtube.com/watch?v=" + video_ids[0]

    @staticmethod
    async def create_playlist(url):
        youtube = build('youtube', 'v3', developerKey=os.environ.get("YOUTUBE_API_KEY"))

        url = url.split("list=")
        playlist_id = url[1].split("&")[0]

        videos = []

        nextPageToken = None
        while True:
            pl_request = youtube.playlistItems().list(
                part='contentDetails',
                playlistId=playlist_id,
                maxResults=50,
                pageToken=nextPageToken
            )
            try:
                pl_response = pl_request.execute()
            except HttpError as err:
                raise HttpError(err.resp, err.content) from err

            vid_ids = []
            for item in pl_response['items']:
                vid_ids.append(item['contentDetails']['videoId'])

            vid_request = youtube.videos().list(
                part="statistics",
                id=','.join(vid_ids)
            )

            vid_response = vid_request.execute()

            for item in vid_response['items']:
                vid_views = item['statistics']['viewCount']

                vid_id = item['id']
                yt_link = f'https://youtu.be/{vid_id}'

                videos.append(yt_link)

            nextPageToken = pl_response.get('nextPageToken')

            if not nextPageToken:
                break

        return videos
        