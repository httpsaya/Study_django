# routing.py
from django.urls import path
from .consumers import WSConsumer

websocket_urlpatterns = [
    path('ws/video/<int:video_id>/', WSConsumer.as_asgi())
]