from essentials.commands.music.play import PlayCommand
from essentials.commands.network.connect import ConnectCommand
from essentials.commands.network.disconnect import DisconnectCommand
from essentials.music.song import Song

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
    
    async def play(self, ctx, url):
        if not self.get_server(ctx.guild.id):
            await self.connect(ctx)
        cmd = PlayCommand(ctx,self,url)
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