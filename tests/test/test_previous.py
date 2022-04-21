import logging
import unittest
from unittest.mock import MagicMock

from utility.mockups import *
from essentials.music.musicbot import MusicBot
from essentials.commands.music.previous import PreviousCommand
from essentials.commands.music.skip import SkipCommand
from essentials.music.audioplayer import AudioPlayer

class TestPreviousCommand(unittest.TestCase):
    error_messages = {
        'no_server': 'I am not on any voice channel!',
        'member_not_on_voice': 'You have to be in a voice channel to play the previous song!',
        'no_song': 'There are no songs that have been played before!',
        'not_the_same_text_channel': 'Commands can be accessed from {0}!',
        'not_the_same_voice_channel': 'We are not in the same room!'
    }   
    def setUp(self):
        self.bot = MockBot()
        self.music_bot = MusicBot(bot)

    def test_previous_basic(self):
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
        first_song = unittest.mock.MagicMock()
        second_song = unittest.mock.MagicMock()
        audio_player.add_to_playlist(second_song)
        audio_player.previous_songs.append(first_song)
        command = PreviousCommand(ctx, self.music_bot)
        response = asyncio.run(command.run(logging=False))
        self.assertIsNone(response)
        self.assertTrue(audio_player.get_current_song() == None and audio_player.playlist[1] == first_song and audio_player.playlist[2] == second_song)
        mock_voice_client.stop.assert_called()

    def test_previous_no_server(self):
        ctx = MockContext()
        command = PreviousCommand(ctx, self.music_bot)
        result = asyncio.run(command.run(logging=False))
        self.assertEqual(result, self.error_messages['no_server'])

    def test_previous_member_not_on_voice(self):
        author = MockMember(voice=None)
        ctx = MockContext(author=author)
        server = {'voice_channel': ctx.voice.channel, 'text_channel': ctx.channel, 'audio_player': AudioPlayer(MockVoiceClient())}
        self.music_bot.add_server(ctx.guild.id,server) 
        command = PreviousCommand(ctx,self.music_bot)
        result = asyncio.run(command.run(logging=False))
        self.assertEqual(result, self.error_messages['member_not_on_voice'])
        self.assertTrue(self.music_bot.get_server(ctx.guild.id))

    def test_previous_no_song(self):
        ctx = MockContext()
        server = {'voice_channel': ctx.voice.channel, 'text_channel': ctx.channel, 'audio_player': AudioPlayer(MockVoiceClient())}
        self.music_bot.add_server(ctx.guild.id,server)
        command = PreviousCommand(ctx,self.music_bot)
        result = asyncio.run(command.run(logging=False))
        self.assertEqual(result, self.error_messages['no_song'])
        self.assertTrue(self.music_bot.get_server(ctx.guild.id))

    def test_previous_not_the_same_text_channel(self):
        voice_channel = MockVoiceChannel(id=69, name='asd')
        text_channel = MockTextChannel(id=420)
        audio_player = AudioPlayer(MockVoiceClient())
        audio_player.previous_songs.append(unittest.mock.MagicMock())
        server = {'voice_channel': voice_channel, 'text_channel': text_channel, 'audio_player': audio_player}
        audio_player.add_to_playlist(unittest.mock.MagicMock())
        self.music_bot.add_server(MockGuild().id,server) 
        ctx = MockContext()
        command = PreviousCommand(ctx,self.music_bot)
        result = asyncio.run(command.run(logging=False))
        self.assertEqual(result, self.error_messages['not_the_same_text_channel'].format(text_channel.name))
        self.assertTrue(self.music_bot.get_server(ctx.guild.id))

    def test_previous_not_the_same_voice_channel(self):
        voice_channel = MockVoiceChannel(id=69, name='asd')
        audio_player = AudioPlayer(MockVoiceClient())
        audio_player.previous_songs.append(unittest.mock.MagicMock())
        server = {'voice_channel': voice_channel, 'text_channel': text_channel, 'audio_player': audio_player}
        audio_player.add_to_playlist(unittest.mock.MagicMock())
        self.music_bot.add_server(MockGuild().id, server)
        ctx = MockContext()
        command = PreviousCommand(ctx,self.music_bot)
        result = asyncio.run(command.run(logging=False))
        self.assertEqual(result, self.error_messages['not_the_same_voice_channel'])
        self.assertTrue(self.music_bot.get_server(ctx.guild.id))
