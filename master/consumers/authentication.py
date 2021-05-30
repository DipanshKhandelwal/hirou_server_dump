from channels.auth import AuthMiddlewareStack
from rest_framework.authtoken.models import Token
from urllib.parse import parse_qs
from channels.db import database_sync_to_async


@database_sync_to_async
def get_user_from_token(token):
    try:
        token_db = Token.objects.get(key=token)
        return token_db.user
    except Token.DoesNotExist:
        return None


class TokenAuthMiddleware:
    """
    Token authorization middleware for Django Channels 2
    """

    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        try:
            qs = scope['query_string']
            token = parse_qs(qs.decode()).get('token')
            user = await get_user_from_token(token[0])

            if user is not None:
                scope['user'] = user
            else:
                scope['user'] = None

            return await self.app(scope, receive, send)
        except Exception as exc:
            raise exc

def TokenAuthMiddlewareStack(inner): return TokenAuthMiddleware(
    AuthMiddlewareStack(inner))
