from abc import abstractmethod

from utils.logger import Logger

# Egy rövid magyarázat a run függvényhez:
# A run függvény végig iterál az összes elemen, ami a required_permissionsben van.
# Ha a requirement NEM TELJESÜL, akkor elküldi a hozzá tartozó üzenetet.
# Ez egy két elemű tuple-ökből álló lista, az első elem a requirement, aminek TELJESÜLNIE kell, a második eleme pedig az error message, ha nem teljesülne.

class BaseCommand:
    def __init__(self, ctx, required_permissions, response) -> None:
        self.ctx = ctx
        self.required_permissions = required_permissions
        self.response = response
        self.messages = []
        pass
    
    async def run(self, logging=True, send_message = True):
        if not self.ctx.channel.guild.me.guild_permissions.send_messages:
            return
        for (requirement, message) in self.required_permissions:
            if not requirement:
                if logging:
                    Logger.error(f'ERROR ({self.__class__.__name__}): {message.title}')
                if send_message:
                    await self.ctx.send(embed = message)
                return message.title
        await self.logic(logging=logging)
        if send_message:
            for res in self.response:
                self.messages.append(await self.ctx.send(embed = res))
        await self.after()

    @abstractmethod
    async def logic(self, logging=True):
        pass
    
    @abstractmethod
    async def after(self):
        pass
