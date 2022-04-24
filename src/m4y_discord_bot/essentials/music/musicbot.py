from essentials.commands.music.loop import LoopCommand
from essentials.commands.music.now_playing import NowPlayingCommand
from essentials.commands.music.pause import PauseCommand
from essentials.commands.music.play import PlayCommand
from essentials.commands.network.connect import ConnectCommand
from essentials.commands.network.disconnect import DisconnectCommand
from essentials.commands.music.skip import SkipCommand
from essentials.commands.music.remove import RemoveCommand
from essentials.commands.music.nightcore import NightcoreCommand
from essentials.commands.music.daycore import DaycoreCommand
from essentials.commands.music.setspeed import SetSpeedCommand
from essentials.commands.music.resetspeed import ResetSpeedCommand
from essentials.commands.music.previous import PreviousCommand
from essentials.commands.lyrics.lyrics import LyricsCommand
from essentials.commands.music.shuffle import ShuffleCommand
from essentials.commands.music.queue import QueueCommand
from essentials.commands.music.bassboost import BassboostCommand
from essentials.music.song import Song
from essentials.commands.music.clear import ClearCommand


class MusicBot:
    def __init__(self, bot) -> None:
        self.bot = bot
        self.servers = {}

    async def connect(self, ctx):
        cmd = ConnectCommand(ctx,self)
        await cmd.run()
        
    async def disconnect(self, ctx):
        cmd = DisconnectCommand(ctx, self)
        await cmd.run()
    
    async def play(self, ctx, url, *args):
        if not self.get_server(ctx.guild.id):
            await self.connect(ctx)
        cmd = PlayCommand(ctx,self,url, *args)
        await cmd.run()

    async def skip(self, ctx):
        cmd = SkipCommand(ctx, self)
        await cmd.run()

    async def loop(self, ctx):
        cmd = LoopCommand(ctx, self)
        await cmd.run()

    async def now_playing(self, ctx):
        cmd = NowPlayingCommand(ctx, self)
        await cmd.run()

    async def pause(self, ctx):
        cmd = PauseCommand(ctx, self)
        await cmd.run()

    async def remove(self, ctx, index):
        cmd = RemoveCommand(ctx, self, index)
        await cmd.run()

    async def nightcore(self, ctx):
        cmd = NightcoreCommand(ctx, self)
        await cmd.run()

    async def daycore(self, ctx):
        cmd = DaycoreCommand(ctx, self)
        await cmd.run()

    async def setspeed(self, ctx, speed):
        cmd = SetSpeedCommand(ctx, self, speed)
        await cmd.run()

    async def resetspeed(self, ctx):
        cmd = ResetSpeedCommand(ctx, self)
        await cmd.run()
    
    async def previous(self, ctx):
        cmd = PreviousCommand(ctx, self)
        await cmd.run()

    async def lyrics(self, ctx, song_title):
        cmd = LyricsCommand(ctx, self, song_title)
        await cmd.run()

    async def shuffle(self, ctx):
        cmd = ShuffleCommand(ctx, self)
        await cmd.run()
    
    async def queue(self, ctx):
        cmd = QueueCommand(ctx, self)
        await cmd.run()

    async def bassboost(self, ctx):
        cmd = BassboostCommand(ctx, self)
        
    async def clear(self, ctx):
        cmd = ClearCommand(ctx, self)
        await cmd.run()

    def add_server(self, id, server):
        self.servers[id] = server

    def clear_server(self, id):
        del self.servers[id]

    def clear_text_channel(self, id):
        self.servers[id]['text_channel'] = None

    def update_voice_channel(self, id, channel):
        try:
            self.servers[id]['voice_channel'] = channel
        except KeyError:
            pass

    def get_server(self, id):
        try:
            return self.servers[id]
        except KeyError:
            return False

    def get_queue_embed(self, server_id):
        try:
            return self.servers[server_id]['queue_message']
        except KeyError:
            return False
