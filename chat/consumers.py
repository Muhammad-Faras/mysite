from channels.generic.websocket import WebsocketConsumer,AsyncWebsocketConsumer
from asgiref.sync import async_to_sync
import json 
import re
import datetime
from .models import ChatGroup, ChatMessage, PrivateChatRoom, PrivateMessage
from accounts.models import Skill
from asgiref.sync import sync_to_async
from django.contrib.auth import get_user_model
from channels.db import database_sync_to_async
User = get_user_model()

class My_WebSocketConsumer(WebsocketConsumer):
    
    def connect(self):
        self.user = self.scope['user']    
        self.user_skill = self.scope['url_route']['kwargs']['userSkill']
        self.group_name = re.sub(r'\W+', '_', self.user_skill)  
        self.timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        if self.user.is_authenticated:    
            async_to_sync(self.channel_layer.group_add)(
                self.group_name,
                self.channel_name
            )
            self.accept()
            self.add_user_to_group()
            
            
           
            
            
        else:
            self.close

    def add_user_to_group(self):
      
        skill, _ = Skill.objects.get_or_create(skill_name=self.user_skill)
        
        
        existing_group = self.user.chatgroup_set.first()
        if existing_group:
           
            existing_group.participants.remove(self.user)
            existing_group.save()
        
   
        chat_group, _ = ChatGroup.objects.get_or_create(skill=skill)
        
       
        chat_group.participants.add(self.user)
        chat_group.save()
        
        self.participants = chat_group.participants.all()
        
       
        self.participant_usernames = [participant.username for participant in self.participants]

        self.send(json.dumps({
            'participants':self.participant_usernames
        }))
        
      
        for participant in self.participants:
            print(participant.username)

       
    def receive(self,text_data=None):
        print('------------------------------------------')
        print('message receive from client/frontend', text_data)
        print('-----------------------------------------')
        # self.send(text_data="message from server")
        data = json.loads(text_data)
        print('-----------------------------------------')
        print('data from client in json format', data)    
        print('-----------------------------------------')
        message = data['msg']
        print('data from client in json format', message)    
        print('-----------------------------------------')
        
        # Create and save ChatMessage instance
        ChatMessage.objects.create(
            group=ChatGroup.objects.get(skill__skill_name=self.user_skill),
            message=message,
            user=self.user,
            timestamp=self.timestamp
        )
        
            
        async_to_sync(self.channel_layer.group_send)(
            self.group_name,
            {
                'type':'chat.message',
                'message':message,
                'user':self.user.username,
                'timestamp':self.timestamp,
                'participants': self.participant_usernames
            }            
        )
        
    def chat_message(self,event):
        print('event.....', event)
        self.send(text_data=json.dumps({
            'msg':event['message'],
            'user':event['user'],
            'timestamp':event['timestamp'],
            'participants': event['participants']
        }))


    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.group_name,
            self.channel_name
        )







class Private_chatroom_Consumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['user']
        self.user2_id = self.scope['url_route']['kwargs']['user2Id']

        self.user2 = await database_sync_to_async(User.objects.get)(id=self.user2_id)

        if self.user.id < self.user2.id:
            self.room_name = f'privatechat_{self.user.id}_{self.user2.id}'
        else:
            self.room_name = f'privatechat_{self.user2.id}_{self.user.id}'
        
        self.chat_room = await database_sync_to_async(self.get_or_create_chat_room)(self.user, self.user2)

        await self.channel_layer.group_add(
            self.room_name,
            self.channel_name
        )

        await self.accept()

    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
            private_message = data.get('msg', '')

            if private_message:
                await database_sync_to_async(self.save_message)(self.user, self.chat_room, private_message)

                await self.channel_layer.group_send(
                    self.room_name,
                    {
                        'type': 'chat_message',
                        'private_message': private_message,
                        'sender': self.user.username
                    }
                )

        except json.JSONDecodeError:
            print('Error decoding JSON')
        except KeyError as e:
            print(f'Key error: {e}')
        except Exception as e:
            print(f'Unexpected error: {e}')

    async def chat_message(self, event):
        private_message = event.get("private_message", "")
        sender = event.get("sender", "")

        await self.send(text_data=json.dumps({
            'private_message': private_message,
            'sender': sender,
        }))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_name,
            self.channel_name,
        )

    def get_or_create_chat_room(self, user1, user2):
        chat_room, created = PrivateChatRoom.objects.get_or_create(
            user1=min(user1, user2, key=lambda u: u.id),
            user2=max(user1, user2, key=lambda u: u.id)
        )
        return chat_room

    def save_message(self, sender, chat_room, message):
        PrivateMessage.objects.create(sender=sender, chat_room=chat_room, message=message)