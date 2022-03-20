import unittest

from utility.mockups import *
from essentials.music.musicbot import MusicBot
from essentials.commands.network.connect import ConnectCommand

class TestConnectCommand(unittest.TestCase):
    error_messages = {
        'already_on_voice': 'I am already in a room!',
        'member_not_on_voice': 'You have to be in a voice channel to summon me!',
        'no_speak_permission': 'I can not speak in there!',
        'no_connect_permission': 'I can not join to you!',
        'user_limit_is_reached': 'The room is full!'
    }   
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

    def test_connection_already_on_voice(self):
        ctx = MockContext()
        voice_channel = ctx.author.voice.channel
        text_channel = ctx.channel
        server = {
            'voice_channel': voice_channel, 
            'text_channel': text_channel
        }
        self.music_bot.add_server(ctx.guild.id, server)
        connect_cmd = ConnectCommand(ctx,self.music_bot)
        result = asyncio.run(connect_cmd.run(logging=False))
        self.assertEqual(result, self.error_messages['already_on_voice'])
        self.assertTrue(self.music_bot.get_server(ctx.guild.id))

    def test_connection_member_not_on_voice(self):
        author = MockMember(voice=None)
        ctx = MockContext(author=author)
        connect_cmd = ConnectCommand(ctx,self.music_bot)
        result = asyncio.run(connect_cmd.run(logging=False))
        self.assertEqual(result, self.error_messages['member_not_on_voice'])
        self.assertFalse(self.music_bot.get_server(ctx.guild.id))

    def test_connection_no_speak_permission(self):
        guild_permissions=MockPermissions(speak=False)
        me = MockMember(guild_permissions=guild_permissions)
        guild = MockGuild(me=me)
        ctx = MockContext(channel=MockTextChannel(guild=guild))
        connect_cmd = ConnectCommand(ctx,self.music_bot)
        result = asyncio.run(connect_cmd.run(logging=False))
        self.assertEqual(result, self.error_messages['no_speak_permission'])
        self.assertFalse(self.music_bot.get_server(ctx.guild.id))
        
    def test_connection_no_connect_permission(self):
        guild_permissions=MockPermissions(connect=False)
        me = MockMember(guild_permissions=guild_permissions)
        guild = MockGuild(me=me)
        ctx = MockContext(channel=MockTextChannel(guild=guild))
        connect_cmd = ConnectCommand(ctx,self.music_bot)
        result = asyncio.run(connect_cmd.run(logging=False))
        self.assertEqual(result, self.error_messages['no_connect_permission'])
        self.assertFalse(self.music_bot.get_server(ctx.guild.id))

    def test_connection_no_user_limit(self):
        channel = MockVoiceChannel(user_limit=0)
        voice = MockVoiceState(channel=channel)
        author = MockMember(voice=voice)
        ctx = MockContext(author=author)
        connect_cmd = ConnectCommand(ctx,self.music_bot)
        asyncio.run(connect_cmd.run(logging=False))
        voice_channel_id = ctx.author.voice.channel.id
        guild_id = ctx.guild.id
        text_channel_id = ctx.channel.id
        server = self.music_bot.get_server(guild_id)
        self.assertEqual(voice_channel_id, server['voice_channel'].id)
        self.assertEqual(text_channel_id, server['text_channel'].id)

    def test_connection_user_limit_is_reached(self):
        channel = MockVoiceChannel(user_limit=1)
        voice = MockVoiceState(channel=channel)
        author = MockMember(voice=voice)
        ctx = MockContext(author=author)
        connect_cmd = ConnectCommand(ctx,self.music_bot)
        result = asyncio.run(connect_cmd.run(logging=False))
        self.assertEqual(result, self.error_messages['user_limit_is_reached'])
        self.assertFalse(self.music_bot.get_server(ctx.guild.id))
