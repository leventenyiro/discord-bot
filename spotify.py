from urllib import response
import requests
from urllib.parse import urlparse

class Spotify:
    def __init__(self, url):
        trackId = urlparse(url).path.split('/')[2]

        # token

        endpoint = 'https://api.spotify.com/v1/tracks/'
        headers = {'Authorization': 'Bearer BQBeWuhSjgkX8j9yeZSacpS7XdaO0rWCNeT-Oznqqv0FW3z5L0nGGax4yOuUSghlEQ9ZSFUSlypEMW3CJ9K2MAvFC_wnET7_dRLrttFQilKe2cCTFqMMWP94IfdiRxXff889DhykthI6Jcsg44o7t-QRH0Y'}

        newUrl = endpoint + trackId

        self.response = requests.get(newUrl, headers=headers)
        print(self.response.json())

    def getTrack(self):
        print(self.response.json())
        


#url = "https://open.spotify.com/track/0UpFAK2INHCzYwhYKwTusv?si=28fa0a3b23814811"
#trackId = urlparse(url).path.split('/')[2]

# query
#endpoint = 'https://api.spotify.com/v1/tracks/'
#headers = {'Authorization': 'Bearer BQBeWuhSjgkX8j9yeZSacpS7XdaO0rWCNeT-Oznqqv0FW3z5L0nGGax4yOuUSghlEQ9ZSFUSlypEMW3CJ9K2MAvFC_wnET7_dRLrttFQilKe2cCTFqMMWP94IfdiRxXff889DhykthI6Jcsg44o7t-QRH0Y'}

#newUrl = endpoint + trackId

