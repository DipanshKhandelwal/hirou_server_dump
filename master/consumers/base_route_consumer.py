from .constants import SocketChannels
from master.models import BaseRoute
from asgiref.sync import sync_to_async
from .helpers import get_channel_group_name
from .route_consumer import RouteConsumer


class BaseRouteConsumer(RouteConsumer):
    def get_route_id(self):
        return self.scope["url_route"]["kwargs"]["base_route_id"]

    def get_group_name(self):
        return get_channel_group_name(SocketChannels.BASE_ROUTE, self.get_route_id())

    async def is_id_valid(self):
        await sync_to_async(BaseRoute.objects.get)(id=self.get_route_id())
