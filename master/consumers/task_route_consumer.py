from urllib.parse import parse_qs
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from .constants import SocketChannels
from .constants import SocketChannels, SocketKeys, SocketEventTypes, SocketSubEventTypes, SocketUpdateTypes
from master.models import User, TaskRoute
from users.models import Profile
from asgiref.sync import sync_to_async
from .helpers import get_channel_group_name


class TaskRouteConsumer(AsyncJsonWebsocketConsumer):
    def get_task_route_id(self):
        return self.scope["url_route"]["kwargs"]["task_route_id"]

    def get_group_name(self):
        return get_channel_group_name(SocketChannels.TASK_ROUTE, self.get_task_route_id())

    async def connect(self):
        try:
            await sync_to_async(TaskRoute.objects.get)(id=self.get_task_route_id())
            await self.accept()
            await self.channel_layer.group_add(self.get_group_name(), self.channel_name)
            await self.send_json({'success': True})
        except TaskRoute.DoesNotExist:
            print("disconnect")
            await self.close()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.get_group_name(), self.channel_name)
        await self.send_json({'success': True})
        await self.close()

    async def websocket_ingest(self, event):
        data = event['data']
        if data:
            await self.send_json(data)

    async def receive_json(self, content, **kwargs):
        event = content[SocketKeys.EVENT]
        sub_event = content[SocketKeys.SUB_EVENT]
        data = content[SocketKeys.DATA]

        if event == SocketEventTypes.LOCATION:
            if sub_event == SocketSubEventTypes.UPDATE:

                if not data:
                    await self.disconnect()
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

        pass
