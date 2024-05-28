from django.shortcuts import render,redirect,HttpResponse
from .forms import AuthenticationFormExtended
from django.contrib.auth import authenticate, login, logout

# Create your views here.
def custom_404_view_name(request,exception):
    return render(request, '404.html',)

def terms_of_service_view(request):
    return render(request, 'terms_of_service.html')


def privacy_policy_view(request):
    return render(request, 'privacy_policy.html')

def home_view(request):
    if request.method == 'POST':
        form = AuthenticationFormExtended(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                # Redirect to a success page or wherever you want
                return redirect('feed:feed')
            else:
                # Return an 'invalid login' error message.
                return redirect('home:home')
    else:
        form = AuthenticationFormExtended()
    return render(request, 'home/home.html', {'form': form})