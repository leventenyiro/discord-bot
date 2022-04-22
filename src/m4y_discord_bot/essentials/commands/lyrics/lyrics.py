from essentials.commands.base_command import BaseCommand
from utils.logger import Logger
from utils.embeds import InfoEmbed
from external.lyrics.lyrics import Lyrics

class LyricsCommand(BaseCommand):
    def __init__(self, ctx, music_bot, song_title, **kw) -> None:
        self.music_bot = music_bot
        self.ctx = ctx

        title = " "
        if song_title != None:
            title = title.join(song_title)
        self.lyrics_object = kw.get('lyrics', Lyrics)
        self.lyrics = self.lyrics_object.get_lyrics(title)

        self.server = music_bot.get_server(ctx.channel.guild.id)
        try:
            text_channel = self.server['text_channel']
        except Exception:
            text_channel = None
        try:
            voice_channel = self.server['voice_channel']
        except Exception:
            voice_channel = None
        required_permissions = [
            (self.server, InfoEmbed('I am not on any voice channel!')),
            (ctx.author.voice is not None, InfoEmbed('You have to be in a voice channel to get lyrics of the music!')),
            (self.lyrics["full_title"] is not None and self.lyrics["url"] is not None, InfoEmbed(f'I have not find any lyrics of {song_title}!')),
            (text_channel is not None and ctx.channel.id == text_channel.id, InfoEmbed(f'Commands can be accessed from {text_channel.name if text_channel is not None else None}!')),
            (ctx.author.voice is not None and voice_channel is not None and ctx.author.voice.channel.id == voice_channel.id, InfoEmbed('We are not in the same room!'))
        ]
        response = [
            InfoEmbed(f'Here is the lyrics link of {self.lyrics["full_title"]}: {self.lyrics["url"]}')
        ]
        super().__init__(ctx, required_permissions, response)
    
    async def logic(self, logging=True):
        if logging:
            Logger.info(f'Request on {self.ctx.guild.id}.')
