import math
import unittest
from unittest.mock import MagicMock

from essentials.commands.music.now_playing import NowPlayingCommand
from utility.mockups import *
from essentials.music.musicbot import MusicBot
from essentials.music.audioplayer import AudioPlayer

class TestNowPlaying(unittest.TestCase):
    error_messages = {
        'no_server': 'I am not on any voice channel!',
        'no_song': 'There is no song currently playing!',
        'not_the_same_text_channel': 'Commands can be accessed from {0}!'
    }
    def setUp(self):
        self.bot = MockBot()
        self.music_bot = MusicBot(bot)
        self.song = MockSong()

    def test_now_playing_basic(self):
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
        command = NowPlayingCommand(ctx, self.music_bot)
        response = asyncio.run(command.run(logging=False))
        self.assertIsNone(response)

    def test_now_playing_no_server(self):
        ctx = MockContext()
        command = NowPlayingCommand(ctx, self.music_bot)
        result = asyncio.run(command.run(logging=False))
        self.assertEqual(result, self.error_messages['no_server'])

    def test_now_playing_no_song(self):
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
        command = NowPlayingCommand(ctx, self.music_bot)
        response = asyncio.run(command.run(logging=False))
        self.assertEqual(response, self.error_messages['no_song'])

    def test_now_playing_not_the_same_text_channel(self):
        voice_channel = MockVoiceChannel(id=69, name='asd')
        text_channel = MockTextChannel(id=420)
        audio_player = AudioPlayer(MockVoiceClient())
        server = {'voice_channel': voice_channel, 'text_channel': text_channel, 'audio_player': audio_player}
        audio_player.add_to_playlist(self.song)
        self.music_bot.add_server(MockGuild().id,server) 
        ctx = MockContext()
        command = NowPlayingCommand(ctx,self.music_bot)
        result = asyncio.run(command.run(logging=False))
        self.assertEqual(result, self.error_messages['not_the_same_text_channel'].format(text_channel.name))
        self.assertTrue(self.music_bot.get_server(ctx.guild.id))
