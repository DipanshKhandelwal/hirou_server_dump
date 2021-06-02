from .constants import SocketChannels
from master.models import TaskRoute
from asgiref.sync import sync_to_async
from .helpers import get_channel_group_name
from .route_consumer import RouteConsumer


class TaskRouteConsumer(RouteConsumer):
    def get_route_id(self):
        return self.scope["url_route"]["kwargs"]["task_route_id"]

    def get_group_name(self):
        return get_channel_group_name(SocketChannels.TASK_ROUTE, self.get_route_id())

    async def is_id_valid(self):
        await sync_to_async(TaskRoute.objects.get)(id=self.get_route_id())
