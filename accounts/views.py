from django.shortcuts import render,redirect,get_object_or_404,HttpResponse
# from .forms import UserCreationFormExtended, AuthenticationFormExtended
from django.contrib.auth import get_user_model
from .forms import ProfileForm
from .models import Profile,Follow,Skill
from allauth.account.views import PasswordChangeView, PasswordSetView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from posts.models import Post
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.core.mail import send_mail
from django.db import IntegrityError
User = get_user_model()

from .models import Profile





@login_required(login_url='/accounts/login/')

def custom_login_redirect(request):
    user = request.user
    profile = Profile.objects.filter(user=user).first()
    if profile is not None and profile.is_complete():
        return redirect('feed:feed')
    else:
        return redirect('accounts:create_profile')
    

@login_required(login_url='/accounts/login/')
def profile_view(request, id):
    context = {}
    
    
    users_you_are_following = User.objects.filter(followers__follower=request.user).count()
    print('------------------------------------------',users_you_are_following)

    users_following_you = User.objects.filter(following__following=request.user).count()
    print('****************************8',users_following_you)
    context = {
        'users_you_are_following': users_you_are_following,
        'users_following_you': users_following_you,
    }
    
    user = get_object_or_404(User, id=id)
    other_user = get_object_or_404(User, id=id)
    is_following = Follow.objects.filter(follower=request.user, following=other_user).exists()
    context = {
        'other_user': other_user,
        'is_following': is_following
    }
     
    print('================')
    print(id)
    try:
        if user.profile.is_complete():
            user_profile = Profile.objects.filter(user=user).first()
            user_posts = Post.objects.filter(author=user)
        else:
            messages.warning(request, 'complete your profile')
            return redirect('accounts:create_profile')
    except:
        
        messages.info(request, 'please! Complete your profile')
        return redirect('accounts:create_profile')

    
    context['user_profile'] = user_profile
    context['user_posts'] = user_posts
    context['users_you_are_following'] = users_you_are_following
    context['users_following_you'] = users_following_you
    
    
    
    print('---------------')
    print(user_profile.user.username)
    print('---------------')
    
    return render(request, 'accounts/profile.html', context)


def about_view(request, user_id):
    user_profile = get_object_or_404(User, id=user_id)
    return render(request, 'accounts/profile_about.html', {'user_profile': user_profile})

@login_required(login_url='/accounts/login/')
def create_profile_view(request):
    context = {}
    
    user=request.user
    try:
        user_profile = Profile.objects.filter(user=user).first()
    except:
        messages.info(request, 'please! Complete your profile')

        return redirect('acccounts:create_profile')


    if user_profile:
        if request.method == 'POST':
            form = ProfileForm(request.POST,request.FILES, instance=user_profile)
            if form.is_valid():
                form.save()
                messages.success(request,'profile operation successfully done')
                return redirect('feed:feed')
            else:
                messages.error(request,'profile updation failed')
                return redirect('accounts:create_profile')
        else:
            form = ProfileForm(instance=user_profile)
    else:
        if request.method == 'POST':
            form = ProfileForm(request.POST, request.FILES)
            if form.is_valid():
                profile = form.save(commit=False)
                profile.user = request.user
                profile.save()
                messages.success(request,'profile operation successfully done')
                return redirect('feed:feed')
            
        else:
            form = ProfileForm()

    context['form'] = form
    return render(request, 'accounts/create_profile.html', context)
    
@login_required(login_url='/accounts/login/')
def other_user_profileview(request, id):
    context = {}
    context['id'] = id
    print('id i get is ',id)
    print('my id is ', request.user.id)
    other_user = get_object_or_404(User, id=id)
    profile = Profile.objects.filter(user=other_user).first()
    context['profile'] = profile
    
    return render(request, 'accounts/other_userprofile.html', context)



class CustomPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    success_url = reverse_lazy('feed:feed')  

    def form_valid(self, form):
        messages.success(self.request, "Password changed successfully.")
        return super().form_valid(form)

    def get_success_url(self):
        
        success_url = self.success_url
        print("Success URL:", success_url)  
        return success_url

    def get(self, *args, **kwargs):
       
        return super().get(*args, **kwargs)

    def post(self, *args, **kwargs):
        
        return super().post(*args, **kwargs)



def follow_view(request,id):
    try:
        other_user = User.objects.get(id=id)
        follow, created = Follow.objects.get_or_create(follower=request.user, following=other_user)
        if created:
            send_mail(
                subject='New Follower Alert!',
                message=f'Hi {other_user.username}, {request.user.username} has started following you.',
                from_email='noorfaras809@gmail.com',
                recipient_list=[other_user.email],
            )
            messages.info(request, f'you successfully followed {other_user.username}')
        return redirect('accounts:profile',id)
    
    except User.DoesNotExist:
        messages.error(request, f"user doesn't exist")
        return redirect('accounts:profile',id)

@login_required
def unfollow_view(request, id):
    try:
        other_user = User.objects.get(id=id)
        follow = Follow.objects.filter(follower=request.user, following=other_user)
        if follow.exists():
            follow.delete()
            
        return redirect('accounts:profile', id=id)
    except User.DoesNotExist:
        return redirect('accounts:profile', id=id)
    