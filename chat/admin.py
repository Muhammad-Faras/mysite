from django.contrib import admin
from .models import ChatGroup, ChatMessage, PrivateMessage, PrivateChatRoom
# Register your models here.

admin.site.register(ChatGroup)
admin.site.register(ChatMessage)
admin.site.register(PrivateMessage)
admin.site.register(PrivateChatRoom)

