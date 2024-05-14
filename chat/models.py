from django.db import models
from accounts.models import Skill
from django.contrib.auth import get_user_model
from accounts.models import Skill
User = get_user_model()
# Create your models here. 

class ChatGroup(models.Model):
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)  # Skill associated with the group
    participants = models.ManyToManyField(User)
    
    
    def __str__(self):
        return self.skill.skill_name
    
    
class ChatMessage(models.Model):
    group = models.ForeignKey(ChatGroup, on_delete=models.CASCADE)  # Reference to the chat group
    message = models.CharField(max_length=1000)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    
class Private_ChatRoom(models.Model):
    user_1 = models.ForeignKey(User,related_name='user1', on_delete=models.CASCADE)
    user_2 = models.ForeignKey(User,related_name='user2', on_delete=models.CASCADE)
    
    
    def __str__(self):
        return f'[{self.user_1}/{self.user_2}]'
    