import logging
import unittest
from unittest.mock import MagicMock

from utility.mockups import *
from essentials.music.musicbot import MusicBot
from essentials.commands.music.queue import QueueCommand
from essentials.music.audioplayer import AudioPlayer

class TestQueueCommand(unittest.TestCase):
    error_messages = {
        'no_server': 'I am not on any voice channel!',
        'no_song': 'There is no song currently playing!',
        'not_the_same_text_channel': 'Commands can be accessed from {0}!',
    }   
    def setUp(self):
        self.bot = MockBot()
        self.music_bot = MusicBot(bot)
        self.song = MockSong()

    def test_queue_basic(self):
        ctx = MockContext()
        voice_channel = ctx.author.voice.channel
        text_channel = ctx.channel
        audio_player = AudioPlayer(MockVoiceClient())
        server = {
            'voice_channel': voice_channel, 
            'text_channel': text_channel,
            'audio_player': audio_player
        }
        self.music_bot.add_server(ctx.guild.id, server)
        audio_player.add_to_playlist(self.song)
        command = QueueCommand(ctx, self.music_bot)
        response = asyncio.run(command.run(logging=False))
        self.assertIsNone(response)
        self.assertIsNone(server['queue_message'])
        self.assertTrue(server['queue_context'])

    def test_queue_no_server(self):
        ctx = MockContext()
        command = QueueCommand(ctx, self.music_bot)
        result = asyncio.run(command.run(logging=False))
        self.assertEqual(result, self.error_messages['no_server'])

    def test_queue_no_song(self):
        ctx = MockContext()
        server = {'voice_channel': ctx.voice.channel, 'text_channel': ctx.channel, 'audio_player': AudioPlayer(MockVoiceClient())}
        self.music_bot.add_server(ctx.guild.id,server)
        command = QueueCommand(ctx,self.music_bot)
        result = asyncio.run(command.run(logging=False))
        self.assertEqual(result, self.error_messages['no_song'])
        self.assertTrue(self.music_bot.get_server(ctx.guild.id))

    def test_queue_not_the_same_text_channel(self):
        voice_channel = MockVoiceChannel(id=69, name='asd')
        text_channel = MockTextChannel(id=420)
        audio_player = AudioPlayer(MockVoiceClient())
        server = {'voice_channel': voice_channel, 'text_channel': text_channel, 'audio_player': audio_player}
        audio_player.add_to_playlist(self.song)
        self.music_bot.add_server(MockGuild().id,server) 
        ctx = MockContext()
        command = QueueCommand(ctx,self.music_bot)
        result = asyncio.run(command.run(logging=False))
        self.assertEqual(result, self.error_messages['not_the_same_text_channel'].format(text_channel.name))
        self.assertTrue(self.music_bot.get_server(ctx.guild.id))
