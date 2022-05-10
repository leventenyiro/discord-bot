import logging
import unittest
from unittest.mock import MagicMock

from utility.mockups import *
from essentials.commands.music.randomize import RandomizeCommand
from essentials.music.musicbot import MusicBot
from essentials.music.audioplayer import AudioPlayer

class TestRandomizeCommand(unittest.TestCase):
    error_messages = {
        'no_server': 'I am not on any voice channel!',
        'no_song': 'There is no song in the playlist!',
        'one_song': 'There is only one song in the playlist!',
        'not_the_same_text_channel': 'Commands can be accessed from {0}!'
    }

    def mock_song(self):
        ret_val = unittest.mock.MagicMock()
        ret_val.url = 'https://youtu.be/'
        ret_val.get_url.return_value = ret_val.url
        return ret_val

    def setUp(self):
        self.bot = MockBot()
        self.music_bot = MusicBot(bot)
        self.first_song = MockSong()
        self.second_song = MockSong()

    def test_randomize_basic(self):
        ctx = MockContext()
        voice_channel = ctx.author.voice.channel
        text_channel = ctx.channel
        mock_voice_client = MockVoiceClient()
        audio_player = AudioPlayer(mock_voice_client)
        server = {
            'voice_channel': voice_channel, 
            'text_channel': text_channel,
            'audio_player': audio_player
        }
        self.music_bot.add_server(ctx.guild.id, server)
        audio_player.add_to_playlist(self.first_song)
        audio_player.add_to_playlist(self.second_song)
        command = RandomizeCommand(ctx, self.music_bot)
        response = asyncio.run(command.run(logging=False))
        self.assertIsNone(response)
    
    def test_randomize_no_song(self):
        ctx = MockContext()
        voice_channel = ctx.author.voice.channel
        text_channel = ctx.channel
        mock_voice_client = MockVoiceClient()
        audio_player = AudioPlayer(mock_voice_client)
        server = {
            'voice_channel': voice_channel, 
            'text_channel': text_channel,
            'audio_player': audio_player
        }
        self.music_bot.add_server(ctx.guild.id, server)
        self.assertTrue(audio_player.get_playlist_length() == 0)
        command = RandomizeCommand(ctx, self.music_bot)
        response = asyncio.run(command.run(logging=False))
        self.assertEqual(response, self.error_messages['no_song'])
        self.assertIsNotNone(response)
        self.assertTrue(audio_player.get_playlist_length() == 0)

    def test_randomize_one_song(self):
        ctx = MockContext()
        voice_channel = ctx.author.voice.channel
        text_channel = ctx.channel
        mock_voice_client = MockVoiceClient()
        audio_player = AudioPlayer(mock_voice_client)
        server = {
            'voice_channel': voice_channel, 
            'text_channel': text_channel,
            'audio_player': audio_player
        }
        self.music_bot.add_server(ctx.guild.id, server)
        audio_player.add_to_playlist(self.first_song)
        self.assertTrue(audio_player.get_playlist_length() == 1)
        command = RandomizeCommand(ctx, self.music_bot)
        response = asyncio.run(command.run(logging=False))
        self.assertEqual(response, self.error_messages['one_song'])
        self.assertIsNotNone(response)
        self.assertTrue(audio_player.get_playlist_length() == 1)
    
    def test_randomize_more_song(self):
        ctx = MockContext()
        voice_channel = ctx.author.voice.channel
        text_channel = ctx.channel
        mock_voice_client = MockVoiceClient()
        audio_player = AudioPlayer(mock_voice_client)
        server = {
            'voice_channel': voice_channel, 
            'text_channel': text_channel,
            'audio_player': audio_player
        }
        self.music_bot.add_server(ctx.guild.id, server)
        audio_player.add_to_playlist(self.first_song)
        self.assertTrue(audio_player.get_playlist_length() == 1)
        audio_player.add_to_playlist(self.second_song)
        self.assertTrue(audio_player.get_playlist_length() == 2)
        command = RandomizeCommand(ctx, self.music_bot)
        response = asyncio.run(command.run(logging=False))
        self.assertIsNone(response)
        self.assertTrue(audio_player.get_playlist_length() == 2) 
    
    def test_randomize_no_server(self):
        ctx = MockContext()
        command = RandomizeCommand(ctx, self.music_bot)
        result = asyncio.run(command.run(logging=False))
        self.assertEqual(result, self.error_messages['no_server'])

    def test_randomize_not_the_same_text_channel(self):
        voice_channel = MockVoiceChannel(id=69, name='asd')
        text_channel = MockTextChannel(id=420)
        audio_player = AudioPlayer(MockVoiceClient())
        server = {'voice_channel': voice_channel, 'text_channel': text_channel, 'audio_player': audio_player}
        self.music_bot.add_server(MockGuild().id,server) 
        ctx = MockContext()
        command = RandomizeCommand(ctx,self.music_bot)
        result = asyncio.run(command.run(logging=False))
        self.assertEqual(result, self.error_messages['not_the_same_text_channel'].format(text_channel.name))
        self.assertTrue(self.music_bot.get_server(ctx.guild.id))
