from django.urls import path

from websocket.consumer import NotificationConsumer

websocket_urlpatterns = [
    path('ws/', NotificationConsumer.as_asgi()),
]
