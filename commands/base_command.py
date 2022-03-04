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
        for (requirement, message) in self.required_permissions:
            if not requirement:
                return await self.ctx.send(message)
        await self.logic()
        for res in self.response:
            await self.ctx.send(res)

    @abstractmethod
    async def logic(self):
        pass