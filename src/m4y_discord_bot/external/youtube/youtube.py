import urllib.request
import re

from urllib.parse import quote

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
        