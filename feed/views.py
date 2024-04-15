from django.shortcuts import render, HttpResponse
from django.contrib.auth.decorators import login_required
# Create your views here.
from posts.models import Post

@login_required(login_url='/accounts/login/')
def feed_view(request):
    context = {}
    posts_list = Post.objects.all()
    
    context['posts_list'] = posts_list
    return render(request, 'feed/feed.html', context)



