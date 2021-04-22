from channels.generic.websocket import AsyncJsonWebsocketConsumer
from .constants import SocketChannels


class UpdateConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        await self.accept()
        await self.send_json({'success': True})

        for channel in SocketChannels.get_all():
            await self.channel_layer.group_add(channel, self.channel_name)

    async def disconnect(self, code):
        for channel in SocketChannels.get_all():
            await self.channel_layer.group_add(channel, self.channel_name)
        await self.send_json({'success': True})
        await self.close()

    async def websocket_ingest(self, event):
        data = event['data']
        if data:
            await self.send_json(data)

    async def receive_json(self, content, **kwargs):
        print("content", content)
        # TODO: Handle subscribe and unsubscribe to channels
        pass
