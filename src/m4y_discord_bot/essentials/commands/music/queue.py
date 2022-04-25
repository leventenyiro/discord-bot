from email.mime import audio
from essentials.commands.base_command import BaseCommand
from utils.logger import Logger
from utils.embeds import InfoEmbed, QueueEmbed

class QueueCommand(BaseCommand):
    def __init__(self, ctx, music_bot) -> None:
        self.music_bot = music_bot
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
            (self.server and self.server['audio_player'].get_playlist_length() > 0, InfoEmbed('There is no song currently playing!')),
            (text_channel is not None and ctx.channel.id == text_channel.id, InfoEmbed(f'Commands can be accessed from {text_channel.name if text_channel is not None else None}!'))
        ]
        try:
            audio_player = self.server['audio_player']
        except Exception:
            audio_player = None
        response = [
            QueueEmbed(audio_player)
        ]
        super().__init__(ctx, required_permissions, response)

    async def logic(self, logging=True):
        pass

    async def after(self):
        queue_message = self.messages[0]
        try:
            await self.server['queue_message'].clear_reactions()
            await self.server['queue_message'].delete()
        except KeyError:
            pass
        self.server['queue_context'] = self.ctx
        audio_player = self.server['audio_player']
        page = audio_player.get_page()
        if page != 0:
            await queue_message.add_reaction(QueueEmbed.REACTIONS[0])
        if page != audio_player.get_max_page()-1:
            await queue_message.add_reaction(QueueEmbed.REACTIONS[1])
        self.server['queue_message'] = queue_message
