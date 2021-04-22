from channels.generic.websocket import AsyncJsonWebsocketConsumer
from .constants import SocketChannels


class UpdateConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        await self.accept()
        await self.send_json({'success': True})

        for channel in SocketChannels.get_all():
            await self.channel_layer.group_add(channel, self.channel_name)

    async def disconnect(self, code):
        await self.close()
