from django.shortcuts import render,redirect,HttpResponse



# Create your views here.
def custom_404_view_name(request,exception):
    return render(request, '404.html',)

def terms_of_service_view(request):
    return render(request, 'terms_of_service.html')


def privacy_policy_view(request):
    return render(request, 'privacy_policy.html')

def home_view(request):
    return render(request, 'home/home.html',)