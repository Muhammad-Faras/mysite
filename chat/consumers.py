from channels.generic.websocket import WebsocketConsumer,AsyncWebsocketConsumer
from asgiref.sync import async_to_sync
import json 
import re
import datetime
from .models import ChatGroup, ChatMessage
from accounts.models import Skill
from asgiref.sync import sync_to_async
from django.contrib.auth import get_user_model
User = get_user_model()

class My_WebSocketConsumer(WebsocketConsumer):
    
    def connect(self):
        self.user = self.scope['user']    
        self.user_skill = self.scope['url_route']['kwargs']['userSkill']
        self.group_name = re.sub(r'\W+', '_', self.user_skill)  # Replace non-alphanumeric characters with underscore
        self.timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        if self.user.is_authenticated:    
            async_to_sync(self.channel_layer.group_add)(
                self.group_name,
                self.channel_name
            )
            self.accept()
            self.add_user_to_group()
            # self.skill = Skill.objects.get(skill_name=self.user_skill)
            # chat_group = ChatGroup.objects.create(skill=self.skill)
            # chat_group.participants.add(self.user)
            # chat_group.save()
            
           
            
            # for g in chat_group:
            #     print(g)
        else:
            self.close

    def add_user_to_group(self):
        # Fetch or create the Skill object based on the skill name
        skill, _ = Skill.objects.get_or_create(skill_name=self.user_skill)
        
        # Check if the user is already in a group for a different skill
        existing_group = self.user.chatgroup_set.first()
        if existing_group:
            # Remove the user from the existing group
            existing_group.participants.remove(self.user)
            existing_group.save()
        
        # Fetch or create the ChatGroup object based on the skill
        chat_group, _ = ChatGroup.objects.get_or_create(skill=skill)
        
        # Add the user to the participants of the ChatGroup
        chat_group.participants.add(self.user)
        chat_group.save()
        
        self.participants = chat_group.participants.all()
        
        # Extract usernames from participants QuerySet
        self.participant_usernames = [participant.username for participant in self.participants]

        self.send(json.dumps({
            'participants':self.participant_usernames
        }))
        
        # Print the usernames of all participants
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
        # Get the current user
        self.user = self.scope['user']

        print('-----------------------------')
        print('username_1 = ', self.user.username)
        print('-----------------------------')

        print('-----------------------------')
        print('username_1.id = ', self.user.id)
        print('-----------------------------')

        # Get user2Id from the URL route
        self.user2_id = self.scope['url_route']['kwargs']['user2Id']

        # Fetch user2 object using user2Id
        self.user2 = await sync_to_async(User.objects.get)(id=self.user2_id)

        print('-----------------------------')
        print('username_2.id = ', self.user2_id)
        print('-----------------------------')

        print('-----------------------------')
        print('username_2 = ', self.user2.username)
        print('-----------------------------')
        if self.user.id < self.user2_id:
            self.group_name = f'privatechat_{self.user.id}_{self.user2.id}'  # Unique group name for the chat between two users
        else:
            self.group_name = f'privatechat_{self.user2.id}_{self.user.id}'  # Unique group name for the chat between two users
        print('-----------------------------')
        print('group_name = ', self.group_name)
        print('-----------------------------')

        # Add both users to the same group
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        # Accept the WebSocket connection
        await self.accept()

    async def receive(self, text_data):
        print('------------------------------------------')
        print('Message received from client/frontend:', text_data)
        print('-----------------------------------------')
        try:
            data = json.loads(text_data)
            print('-----------------------------------------')
            print('Data from client in JSON format:', data)
            print('-----------------------------------------')

            private_message = data['msg']

            print('-----------------------------------------')
            print("Extracting message from data['msg']:", private_message)
            print('-----------------------------------------')

            await self.channel_layer.group_send(
                self.group_name,
                {
                    'type': 'chat_message',
                    'private_message': private_message,
                    'group_name':self.group_name
                }
            )
            print("Sent message to group:", self.group_name)

        except json.JSONDecodeError:
            print('Error decoding JSON')
        except KeyError:
            print('Key error in received data')

    async def chat_message(self, event):
        try:
            print("Event received:", event)
            private_message = event["private_message"]
            group_name = event["group_name"]
            await self.send(text_data=json.dumps({
                'private_message': private_message,
                'group_name': group_name,
            }))
            print("Sent message back to frontend:", private_message)
        except KeyError as e:
            print('Key error in received data:', e)
        except Exception as e:
            print('Error:', e)

    async def disconnect(self, close_code):
        # Remove the user from the group when they disconnect
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )