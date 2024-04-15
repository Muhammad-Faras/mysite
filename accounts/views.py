from django.shortcuts import render,redirect,HttpResponse
# from .forms import UserCreationFormExtended, AuthenticationFormExtended
# from django.contrib.auth import authenticate, login, logout
from .forms import ProfileForm
from .models import Profile


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
                return redirect('accounts:profile')
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
                return HttpResponse('Profile created successfully!')
            else:
                return HttpResponse('Profile creation failed. Please check the form data.')
        else:
            form = ProfileForm()

    context['form'] = form
    return render(request, 'accounts/profile.html', context)





















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