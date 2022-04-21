import unittest
from essentials.commands.music.play import PlayCommand
from essentials.music.audioplayer import AudioPlayer
from essentials.music.musicbot import MusicBot
from utility.mockups import *

class TestPlay(unittest.TestCase):
    error_messages = {
        'member_not_on_voice': 'You have to be in a voice channel to play a song!',
        'song_is_not_correct_format': 'The requested song is not in the correct format!',
        'song_not_found': 'The song was not found!',
        'not_the_same_text_channel': 'Commands can be accessed from {0}!',
        'not_the_same_room': 'We are not in the same room!'
    }

    def setUp(self):
        self.bot = MockBot()
        self.music_bot = MusicBot(bot)
        #self.url = 'https://www.youtube.com/watch?v=2vjPBrBU-TM'
        self.url = None
        self.mocked_song = MockSong()
        self.kwargs = { 'song': self.mocked_song }

    def test_play_basic(self):
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
        command = PlayCommand(ctx, self.music_bot, self.url, **self.kwargs)
        result = asyncio.run(command.run(logging=False))
        self.assertIsNone(result)

    def test_play_member_not_on_voice(self):
        author = MockMember(voice=None)
        ctx = MockContext(author=author)
        command = PlayCommand(ctx, self.music_bot, self.url, **self.kwargs)
        result = asyncio.run(command.run(logging=False))
        self.assertEqual(result, self.error_messages['member_not_on_voice'])
        self.assertFalse(self.music_bot.get_server(ctx.guild.id))

    def test_play_song_is_not_correct_format(self):
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
        command = PlayCommand(ctx, self.music_bot, 'https://www.youtube.com/watch?v=2vjPBrBU-T')
        result = asyncio.run(command.run(logging=False))
        self.assertEqual(result, self.error_messages['song_is_not_correct_format'])

    def test_play_not_the_same_text_channel(self):
        voice_channel = MockVoiceChannel(id=69, name='asd')
        text_channel = MockTextChannel(id=420)
        audio_player = AudioPlayer(MockVoiceClient())
        server = {
            'voice_channel': voice_channel, 
            'text_channel': text_channel,
            'audio_player': audio_player
        }
        self.music_bot.add_server(MockGuild().id,server)
        ctx = MockContext()
        command = PlayCommand(ctx, self.music_bot, self.url, **self.kwargs)
        result = asyncio.run(command.run(logging=False))
        self.assertEqual(result, self.error_messages['not_the_same_text_channel'].format(text_channel.name))
        self.assertTrue(self.music_bot.get_server(ctx.guild.id))

    def test_play_not_the_same_room(self):
        voice_channel = MockVoiceChannel(id=69, name='asd')
        audio_player = AudioPlayer(MockVoiceClient())
        server = {
            'voice_channel1': voice_channel,
            'text_channel': text_channel,
            'audio_player': audio_player
        }
        self.music_bot.add_server(MockGuild().id, server)
        ctx = MockContext()
        command = PlayCommand(ctx, self.music_bot, self.url, **self.kwargs)
        result = asyncio.run(command.run(logging=False))
        self.assertEqual(result, self.error_messages['not_the_same_room'])
        self.assertTrue(self.music_bot.get_server(ctx.guild.id))

    def test_song_not_found(self):
        ctx = MockContext()
        self.mocked_song.failed = True
        voice_channel = ctx.author.voice.channel
        text_channel = ctx.channel
        audio_player = AudioPlayer(MockVoiceClient())
        server = {
            'voice_channel': voice_channel, 
            'text_channel': text_channel,
            'audio_player': audio_player
        }
        self.music_bot.add_server(ctx.guild.id, server)
        command = PlayCommand(ctx, self.music_bot, self.url, **self.kwargs)
        result = asyncio.run(command.run(logging=False))
        self.assertEqual(self.error_messages['song_not_found'], result)
