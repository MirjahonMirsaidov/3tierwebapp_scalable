"""
ASGI config for core project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

import django
import os


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()


from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from websocket.routing import websocket_urlpatterns
from websocket.authentication import QueryAuthMiddleware


application = ProtocolTypeRouter({
  'http': get_asgi_application(),
  'websocket': QueryAuthMiddleware(
    (
      URLRouter(websocket_urlpatterns)
    )
  ),
})
