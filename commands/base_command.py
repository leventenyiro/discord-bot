from abc import abstractmethod

# Egy rövid magyarázat a run függvényhez:
# A run függvény végig iterál az összes elemen, ami a required_permissionsben van.
# Ha a requirement NEM TELJESÜL, akkor elküldi a hozzá tartozó üzenetet.
# Ez egy két elemű tuple-ökből álló lista, az első elem a requirement, aminek TELJESÜLNIE kell, a második eleme pedig az error message, ha nem teljesülne.

class BaseCommand:
    def __init__(self, ctx, required_permissions, response) -> None:
        self.ctx = ctx
        self.required_permissions = required_permissions
        self.response = response
        pass
    
    async def run(self):
        if not self.ctx.channel.guild.me.guild_permissions.send_messages:
            return
        for (requirement, message) in self.required_permissions:
            if not requirement:
                return await self.ctx.send(embed = message)
        await self.logic()
        for res in self.response:
            await self.ctx.send(embed = res)

    @abstractmethod
    async def logic(self):
        pass