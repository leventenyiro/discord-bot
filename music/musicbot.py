from utils.logger import Logger
from utils.promptcolor import PromptColors
from commands.music.connect import ConnectCommand
from commands.music.disconnect import DisconnectCommand

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
    
    def add_server(self, id, server):
        self.servers[id] = server

    def clear_server(self, id):
        del self.servers[id]

    def clear_text_channel(self, id):
        self.servers[id]['text_channel'] = None

    def update_voice_channel(self, id, channel):
        self.servers[id]['voice_channel'] = channel

    def get_server(self, id):
        try:
            return self.servers[id]
        except KeyError:
            return False
