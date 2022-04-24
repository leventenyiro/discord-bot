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
        required_permissions = [
            (self.server and self.server['audio_player'].get_playlist_length() > 1, InfoEmbed('The playlist is empty!'))
            #(text_channel is not None and ctx.channel.id == text_channel.id, InfoEmbed(f'Text channel cleared!'))
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
        player.playlist = [player.get_current_song()]
        
