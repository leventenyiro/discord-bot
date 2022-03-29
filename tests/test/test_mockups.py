import unittest

from utility.mockups import *

class TestMockBot(unittest.TestCase):
    def test_default_values(self):
        bot = MockBot()
        self.assertTrue(bot.guilds)
        self.assertEqual(bot.intents, '')
        self.assertTrue(bot.latency)
        self.assertTrue(bot.loop)
        self.assertTrue(bot.user)
        self.assertTrue(bot.users)

    def test_modify_value(self):
        bot = MockBot()
        self.assertTrue(bot.guilds)
        self.assertEqual(bot.intents, '')
        self.assertTrue(bot.latency)
        self.assertTrue(bot.loop)
        self.assertTrue(bot.user)
        self.assertTrue(bot.users)

        bot = MockBot(
            guilds = 'pass',
            intents = 'asd',
            latency = 0.005,
            loop = 'loop',
            user = 'user',
            users = ['user1', 'user2']
        )

        self.assertEqual(bot.guilds, 'pass')
        self.assertEqual(bot.intents, 'asd')
        self.assertEqual(bot.latency, 0.005)
        self.assertEqual(bot.loop, 'loop')
        self.assertEqual(bot.user, 'user')
        self.assertEqual(bot.users, ['user1', 'user2'])
    
    def test_no_such_attribute(self):
        with self.assertRaises(AttributeError) as error:
            bot = MockBot(asd=123)

class TestMockGuild(unittest.TestCase):
    def test_default_values(self):
        guild = MockGuild()
        self.assertTrue(guild.id)
        self.assertTrue(guild.name)
        self.assertTrue(guild.region)
        self.assertTrue(guild.verification_level)
        self.assertTrue(guild.afk_timeout)
        self.assertTrue(guild.icon)
        self.assertTrue(guild.banner)
        self.assertTrue(guild.mfa_level)
        self.assertTrue(guild.splash)
        self.assertTrue(guild.description)
        self.assertTrue(guild.max_presences)
        self.assertTrue(guild.max_members)
        self.assertTrue(guild.preferred_locale)
        self.assertTrue(guild.owner_id)

    def test_modify_value(self):
        guild = MockGuild()
        self.assertTrue(guild.id)
        self.assertTrue(guild.name)
        self.assertTrue(guild.region)
        self.assertTrue(guild.verification_level)
        self.assertTrue(guild.afk_timeout)
        self.assertTrue(guild.icon)
        self.assertTrue(guild.banner)
        self.assertTrue(guild.mfa_level)
        self.assertTrue(guild.splash)
        self.assertTrue(guild.description)
        self.assertTrue(guild.max_presences)
        self.assertTrue(guild.max_members)
        self.assertTrue(guild.preferred_locale)
        self.assertTrue(guild.owner_id)

        guild = MockGuild(
            id = 2,
            name = 'notguild',
            region = 'Africa',
            verification_level = 3,
            afk_timeout = 50,
            icon = 'sample.png',
            banner = 'sample.png',
            mfa_level = 2,
            splash = 'sample.png',
            description = 'sample',
            max_presences = 10,
            max_members = 10,
            preferred_locale = 'EST',
            owner_id = '2'
        )

        self.assertEqual(guild.id, 2)
        self.assertEqual(guild.name, 'notguild')
        self.assertEqual(guild.region, 'Africa')
        self.assertEqual(guild.verification_level, 3)
        self.assertEqual(guild.afk_timeout, 50)
        self.assertEqual(guild.icon, 'sample.png')
        self.assertEqual(guild.banner, 'sample.png')
        self.assertEqual(guild.mfa_level, 2)
        self.assertEqual(guild.splash, 'sample.png')
        self.assertEqual(guild.description, 'sample')
        self.assertEqual(guild.max_presences, 10)
        self.assertEqual(guild.max_members, 10)
        self.assertEqual(guild.preferred_locale, 'EST')
        self.assertEqual(guild.owner_id, '2')
    
    def test_no_such_attribute(self):
        with self.assertRaises(AttributeError) as error:
            guild = MockGuild(asd=123)

class TestMockVoiceChannel(unittest.TestCase):
    def test_default_values(self):
        voice_channel = MockVoiceChannel()
        self.assertTrue(voice_channel.bitrate)
        self.assertTrue(voice_channel.created_at)
        self.assertTrue(voice_channel.id)
        self.assertTrue(voice_channel.name)
        self.assertTrue(voice_channel.position)
        self.assertTrue(voice_channel.rtc_region)
        self.assertTrue(voice_channel.type)
        self.assertTrue(voice_channel.user_limit)
        self.assertTrue(voice_channel.members)
    
    def test_modify_value(self):
        voice_channel = MockVoiceChannel()
        self.assertTrue(voice_channel.bitrate)
        self.assertTrue(voice_channel.created_at)
        self.assertTrue(voice_channel.id)
        self.assertTrue(voice_channel.name)
        self.assertTrue(voice_channel.position)
        self.assertTrue(voice_channel.rtc_region)
        self.assertTrue(voice_channel.type)
        self.assertTrue(voice_channel.user_limit)
        self.assertTrue(voice_channel.members)

        voice_channel = MockVoiceChannel(
            bitrate = 200,
            created_at = '2021-06-25 07:58:56.550604',
            id = 3,
            name = 'NotGeneral',
            position = 3,
            rtc_region = discord.VoiceRegion.brazil,
            type = discord.ChannelType.text,
            user_limit = 50,
            members = ['hali']
        )

        self.assertEqual(voice_channel.bitrate, 200)
        self.assertEqual(voice_channel.created_at, '2021-06-25 07:58:56.550604')
        self.assertEqual(voice_channel.id, 3)
        self.assertEqual(voice_channel.name, 'NotGeneral')
        self.assertEqual(voice_channel.position, 3)
        self.assertEqual(voice_channel.rtc_region, discord.VoiceRegion.brazil)
        self.assertEqual(voice_channel.type, discord.ChannelType.text)
        self.assertEqual(voice_channel.user_limit, 50)
        self.assertEqual(voice_channel.members, ['hali'])
    
    def test_no_such_attribute(self):
        with self.assertRaises(AttributeError) as error:
            voice_channel = MockVoiceChannel(asd=123)

class TestMockVoiceState(unittest.TestCase):
    def test_default_values(self):
        voice_state = MockVoiceState()
        self.assertFalse(voice_state.afk)
        self.assertFalse(voice_state.deaf)
        self.assertFalse(voice_state.mute)
        self.assertIsNone(voice_state.requested_to_speak_at)
        self.assertFalse(voice_state.self_deaf)
        self.assertFalse(voice_state.self_mute)
        self.assertFalse(voice_state.self_stream)
        self.assertFalse(voice_state.self_video)
        self.assertFalse(voice_state.suppress)

    def test_modify_value(self):
        voice_state = MockVoiceState()
        self.assertFalse(voice_state.afk)
        self.assertFalse(voice_state.deaf)
        self.assertFalse(voice_state.mute)
        self.assertIsNone(voice_state.requested_to_speak_at)
        self.assertFalse(voice_state.self_deaf)
        self.assertFalse(voice_state.self_mute)
        self.assertFalse(voice_state.self_stream)
        self.assertFalse(voice_state.self_video)
        self.assertFalse(voice_state.suppress)

        voice_state = MockVoiceState(
            afk = True,
            deaf = True,
            mute = True,
            requested_to_speak_at = True, 
            self_deaf = True,
            self_mute = True,
            self_stream = True,
            self_video = True,
            suppress = True
        )

        self.assertEqual(voice_state.afk, True)
        self.assertEqual(voice_state.deaf, True)
        self.assertEqual(voice_state.mute, True)
        self.assertEqual(voice_state.requested_to_speak_at, True)
        self.assertEqual(voice_state.self_deaf, True)
        self.assertEqual(voice_state.self_mute, True)
        self.assertEqual(voice_state.self_stream, True)
        self.assertEqual(voice_state.self_video, True)
        self.assertEqual(voice_state.suppress, True)

    def test_no_such_attribute(self):
        with self.assertRaises(AttributeError) as error:
            voice_state = MockVoiceState(asd=123)

class TestMockMember(unittest.TestCase):
    def test_default_values(self):
        member = MockMember()
        self.assertTrue(member.avatar)
        self.assertFalse(member.bot)
        self.assertTrue(member.id)
        self.assertTrue(member.name)
        self.assertTrue(len(member.roles) == 0)
    
    def test_modify_value(self):
        member = MockMember()
        self.assertTrue(member.avatar)
        self.assertFalse(member.bot)
        self.assertTrue(member.id)
        self.assertTrue(member.name)
        self.assertTrue(len(member.roles) == 0)

        member = MockMember(
            avatar = 'enjoyer.jpg',
            bot = True,
            id = 5,
            name = 'kapocsidani',
            roles = ['god']
        )

        self.assertEqual(member.avatar, 'enjoyer.jpg')
        self.assertEqual(member.bot, True)
        self.assertEqual(member.id, 5)
        self.assertEqual(member.name, 'kapocsidani')
        self.assertEqual(member.roles, ['god'])
    
    def test_no_such_attribute(self):
        with self.assertRaises(AttributeError) as error:
            voice_state = MockMember(asd=123)

class TestMockPermissions(unittest.TestCase):
    def test_default_values(self):
        permission = MockPermissions()
        self.assertTrue(permission.add_reactions)
        self.assertFalse(permission.administrator)
        self.assertTrue(permission.attach_files)
        self.assertTrue(permission.ban_members)
        self.assertTrue(permission.change_nickname)
        self.assertTrue(permission.connect)
        self.assertTrue(permission.create_instant_invite)
        self.assertTrue(permission.deafen_members)
        self.assertTrue(permission.embed_links)
        self.assertTrue(permission.external_emojis)
        self.assertTrue(permission.kick_members)
        self.assertTrue(permission.manage_channels)
        self.assertTrue(permission.manage_emojis)
        self.assertTrue(permission.manage_guild)
        self.assertTrue(permission.manage_messages)
        self.assertTrue(permission.manage_nicknames)
        self.assertTrue(permission.manage_permissions)
        self.assertTrue(permission.manage_roles)
        self.assertTrue(permission.manage_webhooks)
        self.assertTrue(permission.mention_everyone)
        self.assertTrue(permission.move_members)
        self.assertTrue(permission.mute_members)
        self.assertTrue(permission.priority_speaker)
        self.assertTrue(permission.read_message_history)
        self.assertTrue(permission.read_messages)
        self.assertTrue(permission.request_to_speak)
        self.assertTrue(permission.send_messages)
        self.assertTrue(permission.send_tts_messages)
        self.assertTrue(permission.speak)
        self.assertTrue(permission.stream)
        self.assertTrue(permission.use_external_emojis)
        self.assertTrue(permission.use_slash_commands)
        self.assertTrue(permission.use_voice_activation)
        self.assertTrue(permission.view_audit_log)
        self.assertTrue(permission.view_channel)
        self.assertTrue(permission.view_guild_insights)
    
    def test_modify_value(self):
        permission = MockPermissions()
        self.assertTrue(permission.add_reactions)
        self.assertFalse(permission.administrator)
        self.assertTrue(permission.attach_files)
        self.assertTrue(permission.ban_members)
        self.assertTrue(permission.change_nickname)
        self.assertTrue(permission.connect)
        self.assertTrue(permission.create_instant_invite)
        self.assertTrue(permission.deafen_members)
        self.assertTrue(permission.embed_links)
        self.assertTrue(permission.external_emojis)
        self.assertTrue(permission.kick_members)
        self.assertTrue(permission.manage_channels)
        self.assertTrue(permission.manage_emojis)
        self.assertTrue(permission.manage_guild)
        self.assertTrue(permission.manage_messages)
        self.assertTrue(permission.manage_nicknames)
        self.assertTrue(permission.manage_permissions)
        self.assertTrue(permission.manage_roles)
        self.assertTrue(permission.manage_webhooks)
        self.assertTrue(permission.mention_everyone)
        self.assertTrue(permission.move_members)
        self.assertTrue(permission.mute_members)
        self.assertTrue(permission.priority_speaker)
        self.assertTrue(permission.read_message_history)
        self.assertTrue(permission.read_messages)
        self.assertTrue(permission.request_to_speak)
        self.assertTrue(permission.send_messages)
        self.assertTrue(permission.send_tts_messages)
        self.assertTrue(permission.speak)
        self.assertTrue(permission.stream)
        self.assertTrue(permission.use_external_emojis)
        self.assertTrue(permission.use_slash_commands)
        self.assertTrue(permission.use_voice_activation)
        self.assertTrue(permission.view_audit_log)
        self.assertTrue(permission.view_channel)
        self.assertTrue(permission.view_guild_insights)

        permission = MockPermissions(
            add_reactions = False,
            administrator = True,
            attach_files = False,
            ban_members = False,
            change_nickname = False,
            connect = False,
            create_instant_invite = False,
            deafen_members = False,
            embed_links = False,
            external_emojis = False,
            kick_members = False,
            manage_channels = False,
            manage_emojis = False,
            manage_guild = False,
            manage_messages = False,
            manage_nicknames = False,
            manage_permissions = False,
            manage_roles = False,
            manage_webhooks = False,
            mention_everyone = False,
            move_members = False,
            mute_members = False,
            priority_speaker = False,
            read_message_history = False,
            read_messages = False,
            request_to_speak = False,
            send_messages = False,
            send_tts_messages = False,
            speak = False,
            stream = False,
            use_external_emojis = False,
            use_slash_commands = False,
            use_voice_activation = False,
            view_audit_log = False,
            view_channel = False,
            view_guild_insights = False,
        )

        self.assertEqual(permission.add_reactions, False)
        self.assertEqual(permission.administrator, True)
        self.assertEqual(permission.attach_files, False)
        self.assertEqual(permission.ban_members, False)
        self.assertEqual(permission.change_nickname, False)
        self.assertEqual(permission.connect, False)
        self.assertEqual(permission.create_instant_invite, False)
        self.assertEqual(permission.deafen_members, False)
        self.assertEqual(permission.embed_links, False)
        self.assertEqual(permission.external_emojis, False)
        self.assertEqual(permission.kick_members, False)
        self.assertEqual(permission.manage_channels, False)
        self.assertEqual(permission.manage_emojis, False)
        self.assertEqual(permission.manage_guild, False)
        self.assertEqual(permission.manage_messages, False)
        self.assertEqual(permission.manage_nicknames, False)
        self.assertEqual(permission.manage_permissions, False)
        self.assertEqual(permission.manage_roles, False)
        self.assertEqual(permission.manage_webhooks, False)
        self.assertEqual(permission.mention_everyone, False)
        self.assertEqual(permission.move_members, False)
        self.assertEqual(permission.mute_members, False)
        self.assertEqual(permission.priority_speaker, False)
        self.assertEqual(permission.read_message_history, False)
        self.assertEqual(permission.read_messages, False)
        self.assertEqual(permission.request_to_speak, False)
        self.assertEqual(permission.send_messages, False)
        self.assertEqual(permission.send_tts_messages, False)
        self.assertEqual(permission.speak, False)
        self.assertEqual(permission.stream, False)
        self.assertEqual(permission.use_external_emojis, False)
        self.assertEqual(permission.use_slash_commands, False)
        self.assertEqual(permission.use_voice_activation, False)
        self.assertEqual(permission.view_audit_log, False)
        self.assertEqual(permission.view_channel, False)
        self.assertEqual(permission.view_guild_insights, False)

    
    def test_no_such_attribute(self):
        with self.assertRaises(AttributeError) as error:
            permission = MockPermissions(asd=123)

class TestMockTextChannel(unittest.TestCase):
    def test_default_values(self):
        channel = MockTextChannel()
        self.assertTrue(channel.id)
        self.assertTrue(channel.type)
        self.assertTrue(channel.name)
        self.assertTrue(channel.topic)
        self.assertTrue(channel.position)
        self.assertFalse(channel.nsfw)
        self.assertTrue(channel.last_message_id)
    
    def test_modify_value(self):
        channel = MockTextChannel()
        self.assertTrue(channel.id)
        self.assertTrue(channel.type)
        self.assertTrue(channel.name)
        self.assertTrue(channel.topic)
        self.assertTrue(channel.position)
        self.assertFalse(channel.nsfw)
        self.assertTrue(channel.last_message_id)

        channel = MockTextChannel(
            id = 2,
            type = 'NotTextChannel',
            name = 'NotGeneral',
            topic = 'nottopic',
            position = 2,
            nsfw = 2,
            last_message_id = 2,
        )

        self.assertEqual(channel.id, 2)
        self.assertEqual(channel.type, 'NotTextChannel')
        self.assertEqual(channel.name, 'NotGeneral')
        self.assertEqual(channel.topic, 'nottopic')
        self.assertEqual(channel.position, 2)
        self.assertEqual(channel.nsfw, 2)
        self.assertEqual(channel.last_message_id, 2)
    
    def test_no_such_attribute(self):
        with self.assertRaises(AttributeError) as error:
            channel = MockTextChannel(asd=123)

class TestMockContext(unittest.TestCase):
    def test_default_values(self):
        context = MockContext()
        self.assertTrue(context.bot)
        self.assertTrue(context.guild)
        self.assertTrue(context.author)
        self.assertTrue(context.channel)
        self.assertTrue(context.voice)

class TestMockVoiceClient(unittest.TestCase):
    def test_mock_voice_client(self):
        voice_client = MockVoiceClient()
        self.assertEqual(voice_client.average_latency, 1)
        self.assertEqual(voice_client.latency, 1)
        self.assertTrue(voice_client.loop)
        self.assertTrue(voice_client.source)
        self.assertEqual(voice_client.token, 'asdasd')
        self.assertTrue(voice_client.user)

    def test_modified_voice_client(self):
        voice_client = MockVoiceClient(latency=69)
        self.assertEqual(voice_client.average_latency, 1)
        self.assertEqual(voice_client.latency, 69)
        self.assertTrue(voice_client.loop)
        self.assertTrue(voice_client.source)
        self.assertEqual(voice_client.token, 'asdasd')
        self.assertTrue(voice_client.user)

    def test_raises_voice_client(self):
        with self.assertRaises(AttributeError) as error:
            voice_client = MockVoiceClient(asd=123)
