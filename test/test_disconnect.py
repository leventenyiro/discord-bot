import unittest

from utils.mockups import *
from music.musicbot import MusicBot
from commands.music.disconnect import DisconnectCommand

class TestDisconnectCommand(unittest.TestCase):
    def test_disconnection_successful(self):
        bot = MockBot()
        music_bot = MusicBot(bot)
        ctx = MockContext()
        music_bot.servers[ctx.guild.id] = {'voice_channel': ctx.voice.channel, 'text_channel': ctx.channel}
        disconnect_cmd = DisconnectCommand(ctx,music_bot)
        asyncio.run(disconnect_cmd.run())
        guild_id = ctx.guild.id
        server = music_bot.get_server(guild_id)
        self.assertFalse(server)
