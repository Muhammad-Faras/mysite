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

from .models import Skill, SubSkill, UserMainSkill, UserSubSkill
from .forms import MainSkillForm, SubSkillForm

@login_required
def main_skill_view(request):
    if request.method == 'POST':
        main_skill_id = request.POST.get('main_skill')
        main_skill =Skill.objects.get(id=main_skill_id)
        UserMainSkill.objects.update_or_create(user=request.user, defaults={'main_skill': main_skill})
        return redirect('accounts:sub_skill')

    main_skills = Skill.objects.all()
    selected_main_skill = None
    try:
        selected_main_skill = request.user.usermainskill.main_skill
    except UserMainSkill.DoesNotExist:
        pass
    return render(request, 'accounts/main_skill.html', {'main_skills': main_skills, 'selected_main_skill': selected_main_skill})

@login_required
def sub_skill_view(request):
    user_main_skill = request.user.usermainskill.main_skill
    sub_skills = SubSkill.objects.filter(main_skill=user_main_skill)

    if request.method == 'POST':
        selected_sub_skills = request.POST.getlist('sub_skills')
        UserSubSkill.objects.filter(user=request.user).delete()
        for sub_skill_id in selected_sub_skills:
            sub_skill = SubSkill.objects.get(id=sub_skill_id)
            UserSubSkill.objects.create(user=request.user, sub_skill=sub_skill)
        return redirect('feed:feed')

    selected_sub_skills = UserSubSkill.objects.filter(user=request.user).values_list('sub_skill', flat=True)
    return render(request, 'accounts/sub_skill.html', {'sub_skills': sub_skills, 'selected_sub_skills': selected_sub_skills})



@login_required(login_url='/accounts/login/')

def custom_login_redirect(request):
    user = request.user
    profile = Profile.objects.filter(user=user).first()
    if profile is not None and profile.is_complete():
        # Redirect to feed page if profile is complete
        return redirect('feed:feed')
    else:
        # Redirect to profile page if profile is not complete
        return redirect('accounts:create_profile')
    

@login_required(login_url='/accounts/login/')
def profile_view(request, id):
    context = {}
    
    
    users_you_are_following = User.objects.filter(followers__follower=request.user).count()
    print('------------------------------------------',users_you_are_following)

    # Users who are following you
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
    #Check if the profile already exists for the user
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
                return redirect('accounts:main_skill')
            else:
                messages.error(request,'profile updation failed')
                return redirect('accounts:create_profile')
        else:
            # Prepopulate the form with existing profile data
            form = ProfileForm(instance=user_profile)
    else:
        if request.method == 'POST':
            form = ProfileForm(request.POST, request.FILES)
            if form.is_valid():
                profile = form.save(commit=False)
                profile.user = request.user
                profile.save()
                messages.success(request,'profile operation successfully done')
                return redirect('accounts:main_skill')
            else:
                messages.error(request,'profile updation failed')
                return redirect('accounts:create_profile')
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
    success_url = reverse_lazy('feed:feed')  # Corrected success URL

    def form_valid(self, form):
        messages.success(self.request, "Password changed successfully.")
        return super().form_valid(form)

    def get_success_url(self):
        # Custom logic for getting success URL if needed
        success_url = self.success_url
        print("Success URL:", success_url)  # Debug message
        return success_url

    def get(self, *args, **kwargs):
        # Custom logic for handling GET requests
        return super().get(*args, **kwargs)

    def post(self, *args, **kwargs):
        # Custom logic for handling POST requests
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
            send_mail(
                subject='Unfollow Notification',
                message=f'Hi {other_user.username}, {request.user.username} has unfollowed you.',
                from_email='your_email@example.com',
                recipient_list=[other_user.email],
            )
        return redirect('accounts:profile', id=id)
    except User.DoesNotExist:
        return redirect('accounts:profile', id=id)
    









# def Student_profile_view(request):
#     if request.method == 'POST':
#         skill_form = StudentProfileForm(request.POST)
#         if skill_form.is_valid():
#             skill = skill_form.cleaned_data['skill']
#             if StudentSkill.objects.filter(user_skill=request.user, skill=skill).exists():
#                 messages.error(request, 'You have already selected this skill.')
#             else:
#                 try:
#                     student_skill = skill_form.save(commit=False)
#                     student_skill.user_skill = request.user
#                     student_skill.save()
#                     messages.success(request, 'Skill selected successfully.')
#                     return redirect('accounts:student_profile_sub_skill')
#                 except IntegrityError:
#                     messages.error(request, 'This skill is already associated with your profile.')
#         else:
#             messages.error(request, 'Invalid form submission.')
#     else:
#         skill_form = StudentProfileForm()

#     context = {
#         'skill_form': skill_form,
#     }
#     return render(request, 'accounts/student_profile_skill.html', context)







# def signup_view(request):
#     if request.method == 'POST':
#         form = UserCreationFormExtended(request.POST)
#         if form.is_valid():
#             form.save()
#             # Redirect to a success page or wherever you want
#             return redirect('posts:posts')
#         else:
#             form = UserCreationFormExtended()
#     else:
#         form = UserCreationFormExtended()
#     return render(request, 'accounts/signup.html', {'form': form})


# def login_view(request):
#     if request.method == 'POST':
#         form = AuthenticationFormExtended(request, request.POST)
#         if form.is_valid():
#             email = form.cleaned_data['email']
#             password = form.cleaned_data['password']
#             user = authenticate(request, email=email, password=password)
#             if user is not None:
#                 login(request, user)
#                 # Redirect to a success page or wherever you want
#                 return redirect('posts:posts')
#             else:
#                 # Return an 'invalid login' error message.
#                 return redirect('home:home')
#     else:
#         form = AuthenticationFormExtended()
# return render(request, 'accounts/login.html', {'form': form})