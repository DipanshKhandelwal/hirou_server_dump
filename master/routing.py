from django.urls import re_path
from .consumers.base_route_consumer import BaseRouteConsumer
from .consumers.task_route_consumer import TaskRouteConsumer


websocket_urlpatterns = [
    re_path(r'^ws/subscribe/base-route/(?P<base_route_id>\w+)/$', BaseRouteConsumer.as_asgi()),
    re_path(r'^ws/subscribe/task-route/(?P<task_route_id>\w+)/$', TaskRouteConsumer.as_asgi()),
]
