from django.shortcuts import render,redirect,HttpResponse, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import get_user_model
from accounts.models import Profile
from django.db.models import Q
from django.contrib.auth.decorators import login_required
User = get_user_model()

@login_required(login_url='/accounts/login/')
def network_view(request):
    context = {}
    user = request.user

    # Fetch the user's profile
    user_profile = Profile.objects.filter(user=user).first()
    if not user_profile:
        messages.warning(request, 'Please complete your profile.')
        return redirect('accounts:create_profile')

    # Fetch users with the same skill and university, excluding the current user
    related_skill_users = Profile.objects.filter(skill=user_profile.skill).exclude(user=user).select_related('user')
    related_uni_users = Profile.objects.filter(university=user_profile.university).exclude(user=user).select_related('user')

    context['related_skill_users'] = related_skill_users
    context['related_uni_users'] = related_uni_users

    # Fetch other users excluding those with the same skill or university, and the current user
    other_users = User.objects.exclude(
        Q(profile__skill=user_profile.skill) |
        Q(pk=request.user.id)
    )

    context['other_users'] = other_users
    context['user_profile'] = user_profile

    # For debugging purposes
    print('same skill ==== ', related_skill_users)
    print('same uni ==== ', related_uni_users)
    print('other users ==== ', other_users)

    return render(request, 'network/network.html', context)



@login_required(login_url='/accounts/login/')
def search_users_view(request):
    context = {}

    if request.method == 'POST':
        search_query = request.POST.get('search-query')
        if search_query:
            search_result = User.objects.filter(
                Q(username__icontains=search_query) |
                Q(profile__university__university_name__icontains=search_query) |
                Q(profile__skill__skill_name__icontains=search_query)
            ).distinct()
            context['search_result'] = search_result
            if search_result.exists():
                context['search_result'] = search_result
                messages.success(request, 'Users searched successfully.')
                return render(request, 'network/user_search.html', context)
            else:
                messages.info(request, 'No users found matching the search query.')
                return redirect('network:network')
        else:
            return redirect('network:network')  
    else:
        return redirect('network:network')
    
    
