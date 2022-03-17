import unittest

from utility.mockups import *
from essentials.musicbot import MusicBot
from essentials.commands.network.connect import ConnectCommand

class TestConnectCommand(unittest.TestCase):
    def setUp(self):
        self.bot = MockBot()
        self.music_bot = MusicBot(bot)
    
    def test_connection_successful(self):
        ctx = MockContext()
        connect_cmd = ConnectCommand(ctx,self.music_bot)
        asyncio.run(connect_cmd.run(logging=False))
        voice_channel_id = ctx.author.voice.channel.id
        guild_id = ctx.guild.id
        text_channel_id = ctx.channel.id
        server = self.music_bot.get_server(guild_id)
        self.assertEqual(voice_channel_id, server['voice_channel'].id)
        self.assertEqual(text_channel_id, server['text_channel'].id)
