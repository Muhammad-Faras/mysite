from django.shortcuts import render, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

user = get_user_model()
# Create your views here.
from posts.models import Post

@login_required(login_url='/accounts/login/')
def feed_view(request):
    context = {}
    posts_list = Post.objects.all()
    
    context['posts_list'] = posts_list
    return render(request, 'feed/feed.html', context)


@login_required(login_url='/accounts/login/')
def search_users_view(request):
    context = {}
    if request.method == 'POST':
        search_query = request.POST.get('searchedquery')
        searched_users = user.objects.filter(username__icontains=search_query) | user.objects.filter(email__icontains=search_query)
        context['search_query'] = search_query
        context['searched_users'] = searched_users
    else:
        result = "invalid"
        context['result'] = result    

    
    return render(request, 'feed/search_users.html', context)
    

