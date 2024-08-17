import jwt
from channels.db import database_sync_to_async

from core import settings
from userprofile.models import UserProfile


class QueryAuthMiddleware:
    """
    Custom middleware (insecure) that takes user IDs from the query string.
    """

    def __init__(self, app):
        # Store the ASGI application we were passed
        self.app = app

    async def __call__(self, scope, receive, send):
        # Look up user from query string (you should also do things like
        # checking if it is a valid user ID, or if scope["user"] is already
        # populated).
        token = await self.get_token(scope)
        user = await self.get_user(token)
        scope['user'] = user

        return await self.app(scope, receive, send)

    async def get_token(self, scope):
        try:
            if scope['query_string'][:5] == b'token':
                return scope["query_string"].decode("utf8").split("=")[1]
        except:
            raise ValueError("Token not found")

    @database_sync_to_async
    def get_user(self, token):
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user = UserProfile.objects.get(id=payload['user_id'])
            return user
        except jwt.ExpiredSignatureError:
            raise ValueError("Token expired")
        except jwt.exceptions.DecodeError:
            raise ValueError("Invalid token")
