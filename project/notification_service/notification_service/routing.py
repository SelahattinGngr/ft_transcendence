from django.urls import path
from src.consumers import NotificationConsumer


websocket_urlpatterns = [
    path('ws/notifications/', NotificationConsumer.as_asgi()),
]
