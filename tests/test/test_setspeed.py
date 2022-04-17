import unittest
from essentials.commands.music.setspeed import SetSpeedCommand
from essentials.music.audioplayer import AudioPlayer
from essentials.music.musicbot import MusicBot
from utility.mockups import *

class TestSetSpeed(unittest.TestCase):
    error_messages = {
        'no_server': 'I am not on any voice channel!',
        'member_not_on_voice': 'You have to be in a voice channel to set speed of the music!',
        'not_the_same_text_channel': 'Commands can be accessed from {0}!',
        'not_the_same_voice_channel': 'We are not in the same room!',
        'speed_out_of_limits': 'Music speed must be between {0} and {1}!'
    }

    def setUp(self):
        self.bot = MockBot()
        self.music_bot = MusicBot(bot)

    def test_setspeed_basic(self):
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
        audio_player.add_to_playlist(unittest.mock.MagicMock())
        command = SetSpeedCommand(ctx, self.music_bot, 1.5)
        result = asyncio.run(command.run(logging=False))
        self.assertEqual(audio_player.SPEED, 1.5)
        self.assertIsNone(result)

    def test_setspeed_no_server(self):
        ctx = MockContext()
        command = SetSpeedCommand(ctx, self.music_bot, 1.5)
        result = asyncio.run(command.run(logging=False))
        self.assertEqual(result, self.error_messages['no_server'])

    def test_setspeed_member_not_on_voice(self):
        author = MockMember(voice=None)
        ctx = MockContext(author=author)
        server = {'voice_channel': ctx.voice.channel, 'text_channel': ctx.channel, 'audio_player': AudioPlayer(MockVoiceClient())}
        self.music_bot.add_server(ctx.guild.id, server) 
        command = SetSpeedCommand(ctx, self.music_bot, 1.5)
        result = asyncio.run(command.run(logging=False))
        self.assertEqual(result, self.error_messages['member_not_on_voice'])
        self.assertTrue(self.music_bot.get_server(ctx.guild.id))

    def test_setspeed_not_the_same_text_channel(self):
        voice_channel = MockVoiceChannel(id=69, name='asd')
        text_channel = MockTextChannel(id=420)
        audio_player = AudioPlayer(MockVoiceClient())
        server = {'voice_channel': voice_channel, 'text_channel': text_channel, 'audio_player': audio_player}
        audio_player.add_to_playlist(unittest.mock.MagicMock())
        self.music_bot.add_server(MockGuild().id, server) 
        ctx = MockContext()
        command = SetSpeedCommand(ctx, self.music_bot, 1.5)
        result = asyncio.run(command.run(logging=False))
        self.assertEqual(result, self.error_messages['not_the_same_text_channel'].format(text_channel.name))
        self.assertTrue(self.music_bot.get_server(ctx.guild.id))

    def test_setspeed_not_the_same_voice_channel(self):
        voice_channel = MockVoiceChannel(id=69, name='asd')
        audio_player = AudioPlayer(MockVoiceClient())
        server = {'voice_channel': voice_channel, 'text_channel': text_channel, 'audio_player': audio_player}
        audio_player.add_to_playlist(unittest.mock.MagicMock())
        self.music_bot.add_server(MockGuild().id, server)
        ctx = MockContext()
        command = SetSpeedCommand(ctx, self.music_bot, 1.5)
        result = asyncio.run(command.run(logging=False))
        self.assertEqual(result, self.error_messages['not_the_same_voice_channel'])
        self.assertTrue(self.music_bot.get_server(ctx.guild.id))

    def test_setspeed_speed_out_of_limits(self):
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
        audio_player.add_to_playlist(unittest.mock.MagicMock())
        command = SetSpeedCommand(ctx, self.music_bot, 100)
        result = asyncio.run(command.run(logging=False))
        self.assertEqual(result, self.error_messages['speed_out_of_limits'].format(SetSpeedCommand.MIN_SPEED, SetSpeedCommand.MAX_SPEED))

        command = SetSpeedCommand(ctx, self.music_bot, -100)
        result = asyncio.run(command.run(logging=False))
        self.assertEqual(result, self.error_messages['speed_out_of_limits'].format(SetSpeedCommand.MIN_SPEED, SetSpeedCommand.MAX_SPEED))
