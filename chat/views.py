from django.shortcuts import render,redirect,get_object_or_404
from accounts.models import Profile
from .models import ChatGroup,ChatMessage,Private_ChatRoom
from django.contrib.auth import get_user_model


User = get_user_model()
# Create your views here.

def chat_view(request):
    context = {}
    user_profile = Profile.objects.get(user = request.user)
    
    if user_profile.is_complete():
        user_skill = user_profile.skill.skill_name
        context['user_skill'] = user_skill
        
        chat_group = ChatGroup.objects.get(skill__skill_name=user_skill)
        
        # Retrieve chat messages for the ChatGroup
        chat_messages = ChatMessage.objects.filter(group=chat_group)
        context['chat_messages'] = chat_messages
        
        print('----------------------------------')
        print('user_skill ======', user_skill)
        print('----------------------------------')
    return render(request, 'chat/chat.html', context)

# def exit_chatgroup_view(request):
#     if request.method == 'POST':
#         chat_groups = ChatGroup.objects.filter(participants=request.user)
        
#         for chat_group in chat_groups:
#             chat_group.participants.remove(request.user)
        
#         return redirect('feed:feed')


def private_chatroom_view(request, user2_id):
    context={}
    user_1 = request.user
    user_2 = get_object_or_404(User, id=user2_id)
    
    private_room = Private_ChatRoom.objects.filter(user_1=user_1, user_2=user_2)
    if not private_room:
        private_room = Private_ChatRoom.objects.create(user_1=user_1, user_2=user_2)
    
    context['user_1'] = user_1
    context['user_2'] = user_2
    context['private_room'] = private_room
    
    return render(request, 'chat/private_chatroom.html', context)