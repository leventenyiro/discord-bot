import logging
import discord
import random

from utils.embeds import InfoEmbed
from utils.logger import Logger
from utils.promptcolor import PromptColors
from essentials.commands.base_command import BaseCommand

class ClearCommand(BaseCommand):
    def __init__(self, ctx, music_bot) -> None:
        self.music_bot = music_bot
        self.ctx = ctx
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
            (ctx.author.voice is not None, InfoEmbed('You have to be in a voice channel to clear the playlist!')),
            (text_channel is not None and ctx.channel.id == text_channel.id, InfoEmbed(f'Commands can be accessed from {text_channel.name if text_channel is not None else None}!')),
            (self.server and self.server['audio_player'].get_playlist_length() != 0, InfoEmbed('There is no song in the playlist!')),
            (self.server and self.server['audio_player'].get_playlist_length() != 1, InfoEmbed('There is only one song in the playlist!'))
        ]
        response = [
            InfoEmbed('Playlist cleared!')
        ]
        super().__init__(ctx, required_permissions, response)

    async def logic(self, logging=True):
        server = self.music_bot.get_server(self.ctx.channel.guild.id)
        player = server['audio_player']
        if logging:
            Logger.info(f'{PromptColors.CGREENBG}{self.ctx.guild.id}{PromptColors.CEND} Playlist cleared!')
        player.clear()
