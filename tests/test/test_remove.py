import unittest
from essentials.commands.music.remove import RemoveCommand
from essentials.music.audioplayer import AudioPlayer
from essentials.music.musicbot import MusicBot
from utility.mockups import *

class TestRemove(unittest.TestCase):
    error_messages = {
        'no_server': 'I am not on any voice channel!',
        'member_not_on_voice': 'You have to be in a voice channel to remove song from playlist!',
        'no_song': 'There is no song currently playing!',
        'not_the_same_text_channel': 'Commands can be accessed from {0}!',
        'not_the_same_voice_channel': 'We are not in the same room!',
        'index_out_of_range': 'Playlist index is out of range!',
        'skip_instead_of_remove': 'You should use skip command instead of this!'
    }

    def setUp(self):
        self.bot = MockBot()
        self.music_bot = MusicBot(bot)

    def test_remove_basic(self):
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
        audio_player.add_to_playlist(unittest.mock.MagicMock())
        self.assertEqual(audio_player.get_playlist_length(), 2)
        command = RemoveCommand(ctx, self.music_bot, 2)
        result = asyncio.run(command.run(logging=False))
        self.assertEqual(audio_player.get_playlist_length(), 1)
        self.assertIsNone(result)

    def test_remove_no_server(self):
        ctx = MockContext()
        command = RemoveCommand(ctx, self.music_bot, 1)
        result = asyncio.run(command.run(logging=False))
        self.assertEqual(result, self.error_messages['no_server'])

    def test_remove_member_not_on_voice(self):
        author = MockMember(voice=None)
        ctx = MockContext(author=author)
        server = {'voice_channel': ctx.voice.channel, 'text_channel': ctx.channel, 'audio_player': AudioPlayer(MockVoiceClient())}
        self.music_bot.add_server(ctx.guild.id, server) 
        command = RemoveCommand(ctx, self.music_bot, 1)
        result = asyncio.run(command.run(logging=False))
        self.assertEqual(result, self.error_messages['member_not_on_voice'])
        self.assertTrue(self.music_bot.get_server(ctx.guild.id))

    def test_remove_no_song(self):
        ctx = MockContext()
        server = {'voice_channel': ctx.voice.channel, 'text_channel': ctx.channel, 'audio_player': AudioPlayer(MockVoiceClient())}
        self.music_bot.add_server(ctx.guild.id,server)
        command = RemoveCommand(ctx, self.music_bot, 1)
        result = asyncio.run(command.run(logging=False))
        self.assertEqual(result, self.error_messages['no_song'])
        self.assertTrue(self.music_bot.get_server(ctx.guild.id))

    def test_remove_not_the_same_text_channel(self):
        voice_channel = MockVoiceChannel(id=69, name='asd')
        text_channel = MockTextChannel(id=420)
        audio_player = AudioPlayer(MockVoiceClient())
        server = {'voice_channel': voice_channel, 'text_channel': text_channel, 'audio_player': audio_player}
        audio_player.add_to_playlist(unittest.mock.MagicMock())
        self.music_bot.add_server(MockGuild().id, server) 
        ctx = MockContext()
        command = RemoveCommand(ctx, self.music_bot, 1)
        result = asyncio.run(command.run(logging=False))
        self.assertEqual(result, self.error_messages['not_the_same_text_channel'].format(text_channel.name))
        self.assertTrue(self.music_bot.get_server(ctx.guild.id))

    def test_remove_not_the_same_voice_channel(self):
        voice_channel = MockVoiceChannel(id=69, name='asd')
        audio_player = AudioPlayer(MockVoiceClient())
        server = {'voice_channel': voice_channel, 'text_channel': text_channel, 'audio_player': audio_player}
        audio_player.add_to_playlist(unittest.mock.MagicMock())
        self.music_bot.add_server(MockGuild().id, server)
        ctx = MockContext()
        command = RemoveCommand(ctx, self.music_bot, 1)
        result = asyncio.run(command.run(logging=False))
        self.assertEqual(result, self.error_messages['not_the_same_voice_channel'])
        self.assertTrue(self.music_bot.get_server(ctx.guild.id))

    def test_remove_index_out_of_range(self):
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
        command = RemoveCommand(ctx, self.music_bot, 0)
        result = asyncio.run(command.run(logging=False))
        self.assertEqual(result, self.error_messages['index_out_of_range'])

        command = RemoveCommand(ctx, self.music_bot, 2)
        result = asyncio.run(command.run(logging=False))
        self.assertEqual(result, self.error_messages['index_out_of_range'])

    def test_remove_skip_instead_of_remove(self):
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
        command = RemoveCommand(ctx, self.music_bot, 1)
        result = asyncio.run(command.run(logging=False))
        self.assertEqual(result, self.error_messages['skip_instead_of_remove'])
