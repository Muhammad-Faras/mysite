from django.shortcuts import render,redirect,HttpResponse
from .forms import UserCreationFormExtended, AuthenticationFormExtended
from django.contrib.auth import authenticate, login, logout



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
#     return render(request, 'signup.html', {'form': form})


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
#     return render(request, 'login.html', {'form': form})