from django.shortcuts import render,redirect,get_object_or_404
from accounts.models import Profile
from .models import ChatGroup,ChatMessage, PrivateChatRoom, PrivateMessage
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages

User = get_user_model()

@login_required(login_url='/accounts/login/')

@login_required(login_url='/accounts/login/')
def leave_group_view(request):
    user = request.user
    user_profile = Profile.objects.get(user=user)
    try:
        user_skill = user_profile.skill.skill_name
    except:
        return redirect('accounts:create_profile')
    skill_group = ChatGroup.objects.filter(skill__skill_name=user_skill).first()
    
    if skill_group:
        if user in skill_group.participants.all():
            skill_group.participants.remove(user)
            messages.info(request, 'You have left the group.')
            remaining_participants = skill_group.participants.all()
            for participant in remaining_participants:
                print('-------------', participant, '------------------')
            
        else:
            skill_group.participants.add(user)
            return redirect('chat:chat')
    # else:
    #     messages.warning(request, 'No group found for your skill.')
    
    # Redirect to a suitable URL after leaving the group
    return redirect('feed:feed')  # Replace 'some_view_name' with the name of the view you want to redirect to.

@login_required
def join_group_view(request):
    user = request.user
    user_profile = Profile.objects.get(user=user)
    user_skill = user_profile.skill.skill_name
    skill_group = get_object_or_404(ChatGroup, skill__skill_name=user_skill)
    
    if user not in skill_group.participants.all():
        skill_group.participants.add(user)
        
        return redirect('chat:chat')

def chat_view(request):
    context = {}
    
    
    
    user = request.user
    user_profile, created = Profile.objects.get_or_create(user=user)
    if created:
        
        return redirect('feed:feed')
    
    
    if user_profile.is_complete():
        user_skill = user_profile.skill.skill_name
        context['user_skill'] = user_skill
    else:
        messages.info(request, 'You need to complete your profile before accessing the Discussion Forum')
        return redirect('accounts:create_profile')
        
    try:
        chat_group = ChatGroup.objects.get(skill__skill_name=user_skill)
    except ChatGroup.DoesNotExist:
        
        chat_group = ChatGroup.objects.create(skill=user_profile.skill)
        
    skill_group = ChatGroup.objects.filter(skill__skill_name=user_skill).first()

    
    if skill_group:
        
        participants = skill_group.participants.all()
        
  
    chat_messages = ChatMessage.objects.filter(group=chat_group)
    print('--------------------')
    print(participants)
    print('--------------------')
        
    context['chat_messages'] = chat_messages
    for message in chat_messages:
        print('-------------',message,'---------------')
    context['participants'] = participants
        
        
    print('----------------------------------')
    print('user_skill ======', user_skill)
    print('----------------------------------')
    
    return render(request, 'chat/chat.html', context)


def private_chatroom_view(request, user2_id):
    context = {}
    user_1 = request.user
    user_2 = get_object_or_404(User, id=user2_id)

   
    chat_room, created = PrivateChatRoom.objects.get_or_create(
        user1=min(user_1, user_2, key=lambda u: u.id),
        user2=max(user_1, user_2, key=lambda u: u.id)
    )
    
    room = PrivateChatRoom.objects.filter(user1=request.user)
    room2 = PrivateChatRoom.objects.filter(user2=request.user) 
    

    rooms = room | room2
    
  
    messages = PrivateMessage.objects.filter(chat_room=chat_room).order_by('timestamp')
    
    
  
    last_message_status = {}
    for r in rooms:
        last_message = PrivateMessage.objects.filter(chat_room=r).order_by('-timestamp').first()
        if last_message and last_message.sender != request.user:
            last_message_status[r.id] = 'new_message'

    context['user_1'] = user_1
    context['user_2'] = user_2
    context['messages'] = messages
    context['room'] = room
    context['room2'] = room2
    context['rooms'] = rooms
    context['last_message_status'] = last_message_status
    
    
    return render(request, 'chat/private_chatroom.html', context)