import unittest

from utility.mockups import *
from essentials.musicbot import MusicBot
from essentials.commands.network.disconnect import DisconnectCommand

class TestDisconnectCommand(unittest.TestCase):
    def setUp(self):
        self.bot = MockBot()
        self.music_bot = MusicBot(bot)
    
    def test_disconnection_successful(self):
        ctx = MockContext()
        self.music_bot.servers[ctx.guild.id] = {'voice_channel': ctx.voice.channel, 'text_channel': ctx.channel}
        disconnect_cmd = DisconnectCommand(ctx,self.music_bot)
        asyncio.run(disconnect_cmd.run(logging=False))
        guild_id = ctx.guild.id
        server = self.music_bot.get_server(guild_id)
        self.assertFalse(server)
