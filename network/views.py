from django.shortcuts import render, HttpResponse
from django.contrib.auth.decorators import login_required
# Create your views here.
from posts.models import Post

@login_required(login_url='/accounts/login/')
def network_view(request):
    return render(request, 'network/network.html',)