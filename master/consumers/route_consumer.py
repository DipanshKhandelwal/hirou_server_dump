from channels.generic.websocket import AsyncJsonWebsocketConsumer
from .constants import SocketKeys, SocketEventTypes, SocketSubEventTypes


class RouteConsumer(AsyncJsonWebsocketConsumer):
    present_users = {}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_route_id(self):
        pass

    def get_group_name(self):
        pass

    async def is_id_valid(self):
        pass

    async def connect(self):
        try:
            await self.is_id_valid()
            await self.accept()
            await self.channel_layer.group_add(self.get_group_name(), self.channel_name)
            await self.send_json({'success': True})
        except:
            await self.close()

    async def disconnect(self, code):
        group = self.get_group_name()
        user = self.scope["user"]
        await self.channel_layer.group_discard(group, self.channel_name)
        await self.send_json({'success': True})

        if RouteConsumer.present_users.get(group, 0) is not 0:
            RouteConsumer.present_users[group].pop(str(user.id), None)
        await self.close()

    async def websocket_ingest(self, event):
        data = event['data']
        if data:
            await self.send_json(data)

    async def locations_update(self, event):
        data = event['data']
        try:
            if data:
                await self.send_json(data)
        except:
            pass

    async def receive_json(self, content, **kwargs):
        try:
            event = content[SocketKeys.EVENT]
            sub_event = content[SocketKeys.SUB_EVENT]
            data = content[SocketKeys.DATA]

            if event == SocketEventTypes.LOCATION and sub_event == SocketSubEventTypes.UPDATE and data:
                user = self.scope["user"]
                group = self.get_group_name()

                if RouteConsumer.present_users.get(group, 0) is 0:
                    RouteConsumer.present_users[group] = {}

                RouteConsumer.present_users[group][str(user.id)] = {
                    "id": user.id,
                    "name": user.username,
                    "location": data['location']
                }

                await self.channel_layer.group_send(group, {
                    'type': 'locations.update',
                    'data': {
                        SocketKeys.EVENT: SocketEventTypes.LOCATION,
                        SocketKeys.SUB_EVENT: SocketSubEventTypes.UPDATE,
                        SocketKeys.DATA: list(RouteConsumer.present_users[group].values()),
                    }
                })
        except:
            pass
