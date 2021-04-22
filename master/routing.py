from django.urls import re_path
from .consumers.update_consumer import UpdateConsumer


websocket_urlpatterns = [
    re_path(r'^ws/updates/$', UpdateConsumer.as_asgi()),
]
