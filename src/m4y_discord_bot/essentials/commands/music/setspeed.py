from essentials.commands.base_command import BaseCommand
from utils.logger import Logger
from utils.embeds import InfoEmbed

class SetSpeedCommand(BaseCommand):
    MAX_SPEED = 2
    MIN_SPEED = 0.5
    
    def __init__(self, ctx, music_bot, speed) -> None:
        self.music_bot = music_bot
        self.server = music_bot.get_server(ctx.channel.guild.id)
        self.speed = float(speed)
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
            (ctx.author.voice is not None, InfoEmbed('You have to be in a voice channel to set speed of the music!')),
            (text_channel is not None and ctx.channel.id == text_channel.id, InfoEmbed(f'Commands can be accessed from {text_channel.name if text_channel is not None else None}!')),
            (ctx.author.voice is not None and voice_channel is not None and ctx.author.voice.channel.id == voice_channel.id, InfoEmbed('We are not in the same room!')),
            (self.server and self.speed >= self.MIN_SPEED and self.speed <= self.MAX_SPEED, InfoEmbed(f'Music speed must be between {self.MIN_SPEED} and {self.MAX_SPEED}!'))
        ]
        response = [
            InfoEmbed(f'Music speed has changed to {self.speed}!')
        ]
        super().__init__(ctx, required_permissions, response)

    async def logic(self, logging=True):
        if logging:
            Logger.info(f'Set music speed to {self.speed} on {self.ctx.channel.guild.id}')
        audio_player = self.server['audio_player']
        audio_player.set_speed(self.speed)
