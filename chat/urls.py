from django.urls import path
from .views import chat_view,private_chatroom_view

app_name = 'chat'
urlpatterns = [
    path('', chat_view, name='chat'),
    path('private-chatroom/<int:user2_id>/',private_chatroom_view , name='private_chatroom')
]