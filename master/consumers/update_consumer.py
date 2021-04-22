from channels.generic.websocket import AsyncJsonWebsocketConsumer


class UpdateConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, code):
        await self.close()
