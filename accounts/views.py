from django.shortcuts import render,redirect,get_object_or_404,HttpResponse
# from .forms import UserCreationFormExtended, AuthenticationFormExtended
from django.contrib.auth import get_user_model
from .forms import ProfileForm
from .models import Profile
from allauth.account.views import PasswordChangeView, PasswordSetView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin


User = get_user_model()

from .models import Profile

def custom_login_redirect(request):
    user = request.user
    profile = Profile.objects.filter(user=user).first()
    if profile is not None and profile.is_complete():
        # Redirect to feed page if profile is complete
        return redirect('feed:feed')
    else:
        # Redirect to profile page if profile is not complete
        return redirect('accounts:profile')
    
    
def profile_view(request):
    context = {}
    user = request.user
    profile = Profile.objects.filter(user=user).first()

    # Check if the profile already exists for the user
    if profile:
        if request.method == 'POST':
            form = ProfileForm(request.POST,request.FILES, instance=profile)
            if form.is_valid():
                form.save()
                return redirect('feed:feed')
            else:
                return HttpResponse('Profile update failed. Please check the form data.')
        else:
            # Prepopulate the form with existing profile data
            form = ProfileForm(instance=profile)
    else:
        if request.method == 'POST':
            form = ProfileForm(request.POST, request.FILES)
            if form.is_valid():
                profile = form.save(commit=False)
                profile.user = request.user
                profile.save()
                return redirect('feed:feed')
            else:
                return HttpResponse('Profile creation failed. Please check the form data.')
        else:
            form = ProfileForm()

    context['form'] = form
    return render(request, 'accounts/profile.html', context)



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
#     return render(request, 'accounts/login.html', {'form': form})