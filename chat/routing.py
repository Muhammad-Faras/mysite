from django.urls import path
from .consumers import My_WebSocketConsumer,Private_chatroom_Consumer

websocket_urlpatterns = [
    path('ws/wsc/<str:userSkill>/', My_WebSocketConsumer.as_asgi()),
    path('ws/wsc/private_chatroom/<int:user2Id>/', Private_chatroom_Consumer.as_asgi()),
]