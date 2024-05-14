from django.contrib import admin
from .models import ChatGroup, ChatMessage, Private_ChatRoom
# Register your models here.

admin.site.register(ChatGroup)
admin.site.register(ChatMessage)
admin.site.register(Private_ChatRoom)
