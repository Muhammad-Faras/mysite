from django.shortcuts import render,redirect, HttpResponse,HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

user = get_user_model()
# Create your views here.
from posts.models import Post,Comment
from posts.forms import CommentForm

@login_required(login_url='/accounts/login/')
def feed_view(request):
    context = {}
    posts_list = Post.objects.all()
    comments = Comment.objects.all()
    
    Comment_form = CommentForm()
# Inside your view function
    if request.method == 'POST':
        Comment_form = CommentForm(request.POST)
        if Comment_form.is_valid():
            post_id = request.POST.get('post_id')
            print('post ki id ya ha = ',post_id)
            post = Post.objects.get(id=post_id)
            comment = Comment_form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('feed:feed')  # Redirect back to the same page


    context['posts_list'] = posts_list
    context['comments'] = comments
    context['Comment_form'] = Comment_form
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
    

