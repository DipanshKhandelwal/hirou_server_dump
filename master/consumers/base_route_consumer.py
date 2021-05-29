from urllib.parse import parse_qs
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from .constants import SocketChannels
from .constants import SocketChannels, SocketKeys, SocketEventTypes, SocketSubEventTypes, SocketUpdateTypes
from master.models import User, BaseRoute
from users.models import Profile
from asgiref.sync import sync_to_async


class BaseRouteConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        try:
            self.base_route_group = "task_route_%s" % self.base_route_id
            self.base_route_id = self.scope["url_route"]["kwargs"]["base_route_id"]
            await sync_to_async(BaseRoute.objects.get)(id=self.base_route_id)
            await self.accept()
            await self.channel_layer.group_add(self.base_route_group, self.channel_name)
            await self.send_json({'success': True})
        except BaseRoute.DoesNotExist:
            await self.close()

    async def disconnect(self, code):
        print("disconnect base")

        # on disconnect clear out the location

        for channel in SocketChannels.get_all():
            await self.channel_layer.group_discard(channel, self.channel_name)
        await self.send_json({'success base': True})
        await self.close()

    async def websocket_ingest(self, event):
        data = event['data']
        if data:
            await self.send_json(data)

    async def receive_json(self, content, **kwargs):
        # try:

        # print("content", content)

        event = content[SocketKeys.EVENT]
        sub_event = content[SocketKeys.SUB_EVENT]
        data = content[SocketKeys.DATA]

        if event == SocketUpdateTypes.SUBSCRIBE:
            print("SUBSCRIBE base")
            if data == SocketChannels.COLLECTION_POINT_CHANNEL:
                await self.channel_layer.group_add(SocketChannels.COLLECTION_POINT_CHANNEL, self.channel_name)
            elif data == SocketChannels.TASK_COLLECTION_POINT_CHANNEL:
                await self.channel_layer.group_add(SocketChannels.TASK_COLLECTION_POINT_CHANNEL, self.channel_name)

        if event == SocketUpdateTypes.UNSUBSCRIBE:
            print("UNSUBSCRIBE base")
            if data == SocketChannels.COLLECTION_POINT_CHANNEL:
                await self.channel_layer.group_discard(SocketChannels.COLLECTION_POINT_CHANNEL, self.channel_name)
            elif data == SocketChannels.TASK_COLLECTION_POINT_CHANNEL:
                await self.channel_layer.group_discard(SocketChannels.TASK_COLLECTION_POINT_CHANNEL, self.channel_name)

        if event == SocketEventTypes.LOCATION:
            # print("event", event)
            # print("sub_event", sub_event)
            # print("data", data)

            if sub_event == SocketSubEventTypes.UPDATE:

                if not data:
                    # for channel in SocketChannels.get_all():
                    #     await self.channel_layer.group_discard(channel, self.channel_name)
                    # await self.send_json({'success': True})
                    # await self.close()
                    return

                user_id = data['id']
                location = data['location']

                # print("user_id", user_id)

                user = await sync_to_async(User.objects.get)(id=user_id)
                profile = await sync_to_async(Profile.objects.get)(user=user)

                profile.location = location

                await sync_to_async(profile.save)()

                # print("user", user)
                # print("location", location)
                # print("profile", profile.bio)

        # except:
        #     print("Error")
        #     pass

        # TODO: Handle subscribe and unsubscribe to channels
        pass
