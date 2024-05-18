from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
# Create your views here.
from django.contrib.auth import get_user_model
from accounts.models import Profile
from django.db.models import Q
User = get_user_model()

@login_required(login_url='/accounts/login/')
def network_view(request):
    context = {}
    try:
        user_profile = Profile.objects.filter(user=request.user).first()
    except Profile.DoesNotExist:
        # Handle the case where the profile does not exist, if needed
        return redirect('accounts:profile')

    if user_profile:
        related_skill_users = Profile.objects.filter(skill=user_profile.skill).exclude(user=request.user).select_related('user')
        related_uni_users = Profile.objects.filter(university=user_profile.university).exclude(user=request.user).select_related('user')
        
        other_users = User.objects.exclude(
            Q(profile__skill=user_profile.skill) |
            Q(profile__university=user_profile.university) |
            Q(pk=request.user.pk)
        )
        
        context['user_profile'] = user_profile
        context['related_skill_users'] = related_skill_users
        context['related_uni_users'] = related_uni_users
        context['other_users'] = other_users
        print('same skill ==== ',related_skill_users)
        print('same uni ==== ',related_uni_users)
        print('other users ==== ', other_users)
    else:
        return redirect('accounts:profile')
    
    
    return render(request, 'network/network.html', context)