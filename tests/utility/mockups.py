import collections
from datetime import datetime
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

bot_data = {
    'guilds': unittest.mock.MagicMock(),
    'intents': '',
    'latency': 0.001,
    'loop': _mocked_loop(asyncio.AbstractEventLoop),
    'user': 'asd',
    'users': ['asd', 'asd2']
}

guild_data = {
    'id': 1,
    'name': 'guild',
    'region': 'Europe',
    'verification_level': 2,
    'afk_timeout': 100,
    'icon': "icon.png",
    'banner': 'banner.png',
    'mfa_level': 1,
    'splash': 'splash.png',
    'description': 'hello world',
    'max_presences': 10000,
    'max_members': 100000,
    'preferred_locale': 'UTC',
    'owner_id': 1,
}

voice_client_data = {
    'average_latency': 1,
    'latency': 1,
    'loop': _mocked_loop(asyncio.AbstractEventLoop),
    'source': unittest.mock.MagicMock(),
    'token': 'asdasd',
    'user': unittest.mock.MagicMock()
}

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

member_data = {
    'avatar': 'avatar.jpg',
    'bot': False,
    'id': 1,
    'name': 'kapocsi',
    'user': 'kapocsi',
    'roles': []
}

permissions_data = {
    'add_reactions': True,
    'administrator': False,
    'attach_files': True,
    'ban_members': True,
    'change_nickname': True,
    'connect': True,
    'create_instant_invite': True,
    'deafen_members': True,
    'embed_links': True,
    'external_emojis': True,
    'kick_members': True,
    'manage_channels': True,
    'manage_emojis': True,
    'manage_guild': True,
    'manage_messages': True,
    'manage_nicknames': True,
    'manage_permissions': True,
    'manage_roles': True,
    'manage_webhooks': True,
    'mention_everyone': True,
    'move_members': True,
    'mute_members': True,
    'priority_speaker': True,
    'read_message_history': True,
    'read_messages': True,
    'request_to_speak': True,
    'send_messages': True,
    'send_tts_messages': True,
    'speak': True,
    'stream': True,
    'use_external_emojis': True,
    'use_slash_commands': True,
    'use_voice_activation': True,
    'view_audit_log': True,
    'view_channel': True,
    'view_guild_insights': True,
}

channel_data = {
    'id': 1,
    'type': 'TextChannel',
    'name': 'General',
    'topic': 'topic',
    'position': 1,
    'nsfw': False,
    'last_message_id': 1,
}

class RedefinedMockMixin:
    child_mock_type = unittest.mock.MagicMock
    additional_spec_asyncs = None
    default = {}
    spec_set = None

    def __init__(self, **kwargs):
        name = kwargs.pop('name', None)
        super().__init__(spec_set=self.spec_set,**collections.ChainMap(kwargs,self.default))
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

bot = commands.Bot(unittest.mock.MagicMock(), data=bot_data)
guild = discord.Guild(data=guild_data, state=unittest.mock.MagicMock())
voice_client = discord.VoiceClient(unittest.mock.MagicMock(), unittest.mock.MagicMock())
voice_channel = discord.VoiceChannel(state=unittest.mock.MagicMock(), guild=unittest.mock.MagicMock(), data=voice_channel_data)
voice_state = discord.VoiceState(data=voice_state_data, channel=unittest.mock.MagicMock())
member = discord.Member(data=member_data, guild=unittest.mock.MagicMock(), state=unittest.mock.MagicMock())
text_channel = discord.TextChannel(state=unittest.mock.MagicMock(), guild=unittest.mock.MagicMock(), data=channel_data)
context = Context(message=unittest.mock.MagicMock(), prefix=unittest.mock.MagicMock())

class MockBot(RedefinedMockMixin, unittest.mock.MagicMock):
    default = bot_data
    spec_set = bot
    def __init__(self, **kw) -> None:
        super().__init__(**kw)

    async def can_run(self, ctx):
        return True


class MockGuild(RedefinedMockMixin, unittest.mock.MagicMock):
    default = guild_data
    spec_set = guild
    def __init__(self, **kw) -> None:
        super().__init__(**kw)
        self.roles = []
        self.me = kw.get('me', MockMember())


class MockVoiceChannel(RedefinedMockMixin, unittest.mock.MagicMock):
    default = voice_channel_data
    spec_set = voice_channel
    def __init__(self, **kw) -> None:
        super().__init__(**kw)


class MockVoiceState(RedefinedMockMixin, unittest.mock.MagicMock):
    default = voice_state_data
    spec_set = voice_state
    def __init__(self, **kw) -> None:
        super().__init__(**kw)
        self.channel = kw.get('channel', MockVoiceChannel())


class MockMember(RedefinedMockMixin, unittest.mock.MagicMock):
    default = member_data
    spec_set = member
    def __init__(self, **kw) -> None:
        self.default.pop('user', None)
        super().__init__(**kw)
        self.voice = kw.get('voice', MockVoiceState())
        self.guild_permissions = kw.get('guild_permissions', MockPermissions())


class MockPermissions(RedefinedMockMixin, unittest.mock.MagicMock):
    default = permissions_data
    spec_set = discord.Permissions.none()
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class MockTextChannel(RedefinedMockMixin, unittest.mock.MagicMock):
    default = channel_data
    spec_set = text_channel
    def __init__(self, **kw) -> None:
        super().__init__(**kw)
        self.guild = kw.get('guild', MockGuild())


class MockVoiceClient(RedefinedMockMixin, unittest.mock.MagicMock):
    default = voice_client_data
    spec_set = voice_client
    def __init__(self, **kw):
        super().__init__(**kw)
        self.channel = kw.get('channel', MockVoiceChannel())
        self.guild = kw.get('guild', MockGuild())


class MockContext(RedefinedMockMixin, unittest.mock.MagicMock):
    def __init__(self, **kw) -> None:
        super().__init__(**kw)
        self.bot = kw.get('bot', MockBot())
        self.guild = kw.get('guild', MockGuild())
        self.author = kw.get('author', MockMember())
        self.channel = kw.get('channel', MockTextChannel())
        self.voice = kw.get('voice', MockVoiceState())
        self.voice_client = kw.get('voice_client', MockVoiceClient())
