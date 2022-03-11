import collections
from datetime import datetime
from email.policy import default
import unittest.mock
import discord
from discord.ext import commands
import asyncio
from discord.ext.commands import Context

async def await_function():
    pass

unittest.mock.MagicMock.__await__ = lambda x: await_function().__await__()

def _mocked_loop(type):
    loop = unittest.mock.create_autospec(spec=type, set=True)
    return loop

class RedefinedMockMixin:
    child_mock_type = unittest.mock.MagicMock
    additional_spec_asyncs = None
    default = {}

    def __init__(self, **kwargs):
        name = kwargs.pop('name', None)
        super().__init__(**kwargs)
        if self.additional_spec_asyncs:
            self._spec_asyncs.extend(self.additional_spec_asyncs)
        if name:
            self.name = name
    
    def _get_child_mock(self, **kw):
        _new_name = kw.get("_new_name")
        if _new_name in self.__dict__['_spec_asyncs']:
            return unittest.mock.AsyncMock(**kw)
        _type = type(self)
        if issubclass(_type, unittest.mock.MagicMock) and _new_name in unittest.mock._async_method_magics:
            klass = unittest.mock.AsyncMock
        else:
            klass = self.child_mock_type
        if self._mock_sealed:
            attribute = "." + kw["name"] if "name" in kw else "()"
            mock_name = self._extract_mock_name() + attribute
            raise AttributeError(mock_name)
        return klass(**kw)

bot_data = {
    'application_id': 123,
    'guilds': unittest.mock.MagicMock(),
    'intents': '',
    'latency': 0.001,
    'loop': _mocked_loop(asyncio.AbstractEventLoop),
    'status': 'asd',
    'user': 'asd',
    'users': ['asd', 'asd2']
}

class MockBot(RedefinedMockMixin, unittest.mock.MagicMock):
    def __init__(self, **kw) -> None:
        super().__init__(**collections.ChainMap(self.default,kw))
        self.latency = 0.001

    async def can_run(self, ctx):
        return True

guild_data = {
    'id': 1,
    'name': 'guild',
    'region': 'Europe',
    'verification_level': 2,
    'default_notications': 1,
    'afk_timeout': 100,
    'icon': "icon.png",
    'banner': 'banner.png',
    'mfa_level': 1,
    'splash': 'splash.png',
    'system_channel_id': 464033278631084042,
    'description': 'hello world',
    'max_presences': 10000,
    'max_members': 100000,
    'preferred_locale': 'UTC',
    'owner_id': 1,
    'afk_channel_id': 464033278631084042,
}

guild = discord.Guild(data=guild_data, state=unittest.mock.MagicMock())
class MockGuild(RedefinedMockMixin, unittest.mock.MagicMock):
    default = guild_data
    def __init__(self, **kw) -> None:
        super().__init__(**collections.ChainMap(self.default,kw))
        self.roles = []
        self.me.guild_permissions.send_messages = kw.get('send_messages', True)
        self.me.guild_permissions.connect = kw.get('connect', True)
        self.me.guild_permissions.speak = kw.get('speak', True)

voice_channel_data = {
    'bitrate': 192,
    'created_at': datetime.now(),
    'id': 2,
    'name': 'General',
    'position': 2,
    'rtc_region': discord.VoiceRegion.amsterdam,
    'type': discord.ChannelType.voice,
    'user_limit': 10000,
    'members': ['szia']
}

class MockVoiceChannel(RedefinedMockMixin, unittest.mock.MagicMock):
    default = voice_channel_data
    def __init__(self, **kw) -> None:
        super().__init__(**collections.ChainMap(self.default,kw))

voice_state_data = {
    'afk': False,
    'deaf': False,
    'mute': False,
    'requested_to_speak_at': None, 
    'self_deaf': False,
    'self_mute': False,
    'self_stream': False,
    'self_video': False,
    'suppress': False
}

class MockVoiceState(RedefinedMockMixin, unittest.mock.MagicMock):
    default = voice_state_data
    def __init__(self, **kw) -> None:
        super().__init__(**collections.ChainMap(self.default,kw))
        self.channel = kw.get('channel', MockVoiceChannel())

member_data = {
    'avatar': 'avatar.jpg',
    'bot': False,
    'id': 1,
    'name': 'kapocsi',
    'user': 'kapocsi',
    'roles': []
}

class MockMember(RedefinedMockMixin, unittest.mock.MagicMock):
    default = member_data
    def __init__(self, **kw) -> None:
        super().__init__(**collections.ChainMap(self.default,kw))
        self.voice = kw.get('voice', MockVoiceState())

channel_data = {
    'id': 1,
    'type': 'TextChannel',
    'name': 'General',
    'parent_id': 6969696969,
    'topic': 'topic',
    'position': 1,
    'nsfw': False,
    'last_message_id': 1,
}
channel = discord.TextChannel(state=unittest.mock.MagicMock(), guild=MockGuild(), data=channel_data)

class MockTextChannel(RedefinedMockMixin, unittest.mock.MagicMock):
    default = channel_data
    def __init__(self, **kw) -> None:
        super().__init__(**collections.ChainMap(self.default,kw))
        self.guild = kw.get('guild', MockGuild())

context = Context(message=unittest.mock.MagicMock(), prefix=unittest.mock.MagicMock())

class MockContext(RedefinedMockMixin, unittest.mock.MagicMock):
    def __init__(self, **kw) -> None:
        super().__init__(**collections.ChainMap(self.default,kw))
        self.bot = kw.get('bot', MockBot())
        self.guild = kw.get('guild', MockGuild())
        self.author = kw.get('author', MockMember())
        self.channel = kw.get('channel', MockTextChannel())
        self.voice = kw.get('voice', MockVoiceState())
