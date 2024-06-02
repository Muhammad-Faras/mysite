from django.urls import path
from .views import chat_view,private_chatroom_view,leave_group_view, join_group_view

app_name = 'chat'
urlpatterns = [
    path('', chat_view, name='chat'),
    path('leave-group/', leave_group_view, name='leave_group'),
    path('leave-group/', join_group_view, name='join_group'),
    path('private-chatroom/<int:user2_id>/',private_chatroom_view , name='private_chatroom')
]