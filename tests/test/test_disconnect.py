import unittest

from utility.mockups import *
from essentials.musicbot import MusicBot
from essentials.commands.network.disconnect import DisconnectCommand

class TestDisconnectCommand(unittest.TestCase):
    error_messages = {
        'no_server': 'I am not on any voice channel!',
        'member_not_on_voice': 'You have to be in a voice channel to disconnect me!',
        'not_the_same_text_channel': 'Commands can be accessed from {0}!',
        'not_the_same_voice_channel': 'We are not in the same room!'
    }
    def setUp(self):
        self.bot = MockBot()
        self.music_bot = MusicBot(bot)
    
    def test_disconnection_successful(self):
        ctx = MockContext()
        server = {'voice_channel': ctx.voice.channel, 'text_channel': ctx.channel}
        self.music_bot.add_server(ctx.guild.id,server) 
        disconnect_cmd = DisconnectCommand(ctx,self.music_bot)
        asyncio.run(disconnect_cmd.run(logging=False))
        guild_id = ctx.guild.id
        server = self.music_bot.get_server(guild_id)
        self.assertFalse(server)

    def test_disconnect_no_server(self):
        ctx = MockContext()
        disconnect_cmd = DisconnectCommand(ctx,self.music_bot)
        result = asyncio.run(disconnect_cmd.run(logging=False))
        self.assertEqual(result, self.error_messages['no_server'])
        self.assertFalse(self.music_bot.get_server(ctx.guild.id))

    def test_disconnect_member_not_on_voice(self):
        author = MockMember(voice=None)
        ctx = MockContext(author=author)
        server = {'voice_channel': ctx.voice.channel, 'text_channel': ctx.channel}
        self.music_bot.add_server(ctx.guild.id,server) 
        disconnect_cmd = DisconnectCommand(ctx,self.music_bot)
        result = asyncio.run(disconnect_cmd.run(logging=False))
        self.assertEqual(result, self.error_messages['member_not_on_voice'])
        self.assertTrue(self.music_bot.get_server(ctx.guild.id))

    def test_disconnect_not_the_same_text_channel(self):
        voice_channel = MockVoiceChannel(id=69, name='asd')
        text_channel = MockTextChannel(id=420)
        server = {'voice_channel': voice_channel, 'text_channel': text_channel}
        self.music_bot.add_server(MockGuild().id,server) 
        ctx = MockContext()
        disconnect_cmd = DisconnectCommand(ctx,self.music_bot)
        result = asyncio.run(disconnect_cmd.run(logging=False))
        self.assertEqual(result, self.error_messages['not_the_same_text_channel'].format(text_channel.name))
        self.assertTrue(self.music_bot.get_server(ctx.guild.id))

    def test_disconnect_not_the_same_voice_channel(self):
        voice_channel = MockVoiceChannel(id=69, name='asd')
        server = {'voice_channel': voice_channel, 'text_channel': text_channel}
        self.music_bot.add_server(MockGuild().id, server)
        ctx = MockContext()
        disconnect_cmd = DisconnectCommand(ctx,self.music_bot)
        result = asyncio.run(disconnect_cmd.run(logging=False))
        self.assertEqual(result, self.error_messages['not_the_same_voice_channel'])
        self.assertTrue(self.music_bot.get_server(ctx.guild.id))
