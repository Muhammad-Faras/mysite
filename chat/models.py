from django.db import models
from accounts.models import Skill
from django.contrib.auth import get_user_model
from accounts.models import Skill
from django.utils import timezone
User = get_user_model()
# Create your models here. 

class ChatGroup(models.Model):
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)  # discussion group
    participants = models.ManyToManyField(User)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.skill.skill_name
    
class ChatMessage(models.Model):
    group = models.ForeignKey(ChatGroup, on_delete=models.CASCADE)  # discussion group messages
    message = models.CharField(max_length=1000)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    


class PrivateChatRoom(models.Model):
    user1 = models.ForeignKey(User, related_name='chat_rooms1', on_delete=models.CASCADE)
    user2 = models.ForeignKey(User, related_name='chat_rooms2', on_delete=models.CASCADE)
    

    class Meta:
        unique_together = ('user1', 'user2')

    def __str__(self):
        return f'ChatRoom between {self.user1} and {self.user2}'
    
    
class PrivateMessage(models.Model):
    chat_room = models.ForeignKey(PrivateChatRoom, related_name='messages', on_delete=models.CASCADE)
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f'Message from {self.sender} at {self.timestamp}'

    def mark_as_read(self):
        self.is_read = True
        self.save()