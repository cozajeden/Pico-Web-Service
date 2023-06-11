from django.urls import path
from .chat_consumer import PicoChatConsumer
from ..urls import app_name

websocket_urlpatterns = [
    path(app_name, PicoChatConsumer.as_asgi()),
]

