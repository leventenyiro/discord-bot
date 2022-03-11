import unittest

from utils.mockups import *
from music.musicbot import MusicBot
from commands.music.connect import ConnectCommand

class TestConnectCommand(unittest.TestCase):
    def test_connection_successful(self):
        bot = MockBot()
        music_bot = MusicBot(bot)
        ctx = MockContext()
        connect_cmd = ConnectCommand(ctx,music_bot)
        asyncio.run(connect_cmd.run())
        voice_channel_id = ctx.author.voice.channel.id
        guild_id = ctx.guild.id
        text_channel_id = ctx.channel.id
        server = music_bot.get_server(guild_id)
        self.assertEqual(voice_channel_id, server['voice_channel'].id)
        self.assertEqual(text_channel_id, server['text_channel'].id)
