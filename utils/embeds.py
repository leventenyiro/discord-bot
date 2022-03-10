from discord import Embed
from discord import Colour

botname = "Music4You"
pfp_link = "https://cdn.discordapp.com/avatars/940645443359092806/12cbd729c419913c0bf3373173ac7c01.png"

class InfoEmbed(Embed):
    def __init__(self, message):
        super().__init__()
        self.color = Colour.from_rgb(34,139,34)
        self.title = message
        self.set_author(name=botname, icon_url=pfp_link)
