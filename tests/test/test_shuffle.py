import unittest
from essentials.commands.music.shuffle import ShuffleCommand
from essentials.music.audioplayer import AudioPlayer
from essentials.music.musicbot import MusicBot
from utility.mockups import *

class TestShuffle(unittest.TestCase):
    error_messages = {
        'no_server': 'I am not on any voice channel!',
        'member_not_on_voice': 'You have to be in a voice channel to shuffle songs in playlist!',
        'not_the_same_text_channel': 'Commands can be accessed from {0}!',
        'not_the_same_voice_channel': 'We are not in the same room!',
    }

    def setUp(self):
        self.bot = MockBot()
        self.music_bot = MusicBot(bot)

    def test_shuffle_basic(self):
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
        command = ShuffleCommand(ctx, self.music_bot)
        result = asyncio.run(command.run(logging=False))
        self.assertTrue(audio_player.is_shuffle())
        self.assertIsNone(result)

    def test_shuffle_no_server(self):
        ctx = MockContext()
        command = ShuffleCommand(ctx, self.music_bot)
        result = asyncio.run(command.run(logging=False))
        self.assertEqual(result, self.error_messages['no_server'])

    def test_shuffle_member_not_on_voice(self):
        author = MockMember(voice=None)
        ctx = MockContext(author=author)
        server = {'voice_channel': ctx.voice.channel, 'text_channel': ctx.channel, 'audio_player': AudioPlayer(MockVoiceClient())}
        self.music_bot.add_server(ctx.guild.id, server) 
        command = ShuffleCommand(ctx, self.music_bot)
        result = asyncio.run(command.run(logging=False))
        self.assertEqual(result, self.error_messages['member_not_on_voice'])
        self.assertTrue(self.music_bot.get_server(ctx.guild.id))

    def test_shuffle_not_the_same_text_channel(self):
        voice_channel = MockVoiceChannel(id=69, name='asd')
        text_channel = MockTextChannel(id=420)
        audio_player = AudioPlayer(MockVoiceClient())
        server = {'voice_channel': voice_channel, 'text_channel': text_channel, 'audio_player': audio_player}
        audio_player.add_to_playlist(unittest.mock.MagicMock())
        self.music_bot.add_server(MockGuild().id, server) 
        ctx = MockContext()
        command = ShuffleCommand(ctx, self.music_bot)
        result = asyncio.run(command.run(logging=False))
        self.assertEqual(result, self.error_messages['not_the_same_text_channel'].format(text_channel.name))
        self.assertTrue(self.music_bot.get_server(ctx.guild.id))

    def test_shuffle_not_the_same_voice_channel(self):
        voice_channel = MockVoiceChannel(id=69, name='asd')
        audio_player = AudioPlayer(MockVoiceClient())
        server = {'voice_channel': voice_channel, 'text_channel': text_channel, 'audio_player': audio_player}
        audio_player.add_to_playlist(unittest.mock.MagicMock())
        self.music_bot.add_server(MockGuild().id, server)
        ctx = MockContext()
        command = ShuffleCommand(ctx, self.music_bot)
        result = asyncio.run(command.run(logging=False))
        self.assertEqual(result, self.error_messages['not_the_same_voice_channel'])
        self.assertTrue(self.music_bot.get_server(ctx.guild.id))
