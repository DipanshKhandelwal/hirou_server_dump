import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hirou_server.settings.development')
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hirou_server.settings.production")
django_asgi_app = get_asgi_application()

from channels.security.websocket import AllowedHostsOriginValidator
from channels.routing import ProtocolTypeRouter, URLRouter
from master.consumers.authentication import TokenAuthMiddlewareStack
import master.routing

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    'websocket': AllowedHostsOriginValidator(
        TokenAuthMiddlewareStack(
            URLRouter(
                master.routing.websocket_urlpatterns
            )
        )
    ),
})
