from django.shortcuts import render,redirect,get_object_or_404
from accounts.models import Profile
from .models import ChatGroup,ChatMessage, PrivateChatRoom, PrivateMessage
from django.contrib.auth import get_user_model


User = get_user_model()
# Create your views here.

def chat_view(request):
    context = {}
    user_profile = Profile.objects.filter(user=request.user).first()
    
    if not user_profile:
        return redirect('accounts:profile')
    
    if user_profile.is_complete():
        user_skill = user_profile.skill.skill_name
        context['user_skill'] = user_skill
        
        try:
            chat_group = ChatGroup.objects.get(skill__skill_name=user_skill)
        except ChatGroup.DoesNotExist:
            # Handle the case where the chat group does not exist
            # You can choose to create a new ChatGroup here if needed
            chat_group = ChatGroup.objects.create(skill=user_profile.skill)
        
        # Retrieve chat messages for the ChatGroup
        chat_messages = ChatMessage.objects.filter(group=chat_group)
        context['chat_messages'] = chat_messages
        
        print('----------------------------------')
        print('user_skill ======', user_skill)
        print('----------------------------------')
    
    return render(request, 'chat/chat.html', context)


def private_chatroom_view(request, user2_id):
    context = {}
    user_1 = request.user
    user_2 = get_object_or_404(User, id=user2_id)

    # Get or create the chat room between the two users
    chat_room, created = PrivateChatRoom.objects.get_or_create(
        user1=min(user_1, user_2, key=lambda u: u.id),
        user2=max(user_1, user_2, key=lambda u: u.id)
    )

    # Retrieve the messages for the chat room
    messages = PrivateMessage.objects.filter(chat_room=chat_room).order_by('timestamp')

    context['user_1'] = user_1
    context['user_2'] = user_2
    context['messages'] = messages
    
    return render(request, 'chat/private_chatroom.html', context)