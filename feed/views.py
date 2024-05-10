from django.shortcuts import render,redirect, HttpResponse,HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

User = get_user_model()
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
    print("Request Path:", request.path_info)
    if request.path_info.startswith('/feed/'):
        if request.method == 'POST':
            search_query = request.POST.get('search-query')
            search_result = Post.objects.filter(title__icontains=search_query)
            context['search_result'] = search_result
            return render(request, 'feed/search.html', context)
        else:
            return redirect('feed:feed')
        
    elif request.path_info.startswith('/network/'):
        print("In Network Condition")
        if request.method == 'POST':
            search_query = request.POST.get('search-query')
            search_result = User.objects.filter(username__icontains=search_query) | User.objects.filter(email__icontains=search_query)
            context['search_result'] = search_result
            return render(request, 'network/search.html', context)
        else:
            return redirect('network:network')
    else:
        print("Debug: Request path:", request.path_info)
        return HttpResponse('Page Not Found')



            # searched_result = user.objects.filter(username__icontains=search_query) | user.objects.filter(email__icontains=search_query)
    #         context['search_query'] = search_query
    #         context['searched_users'] = searched_users
    #     else:
    #         result = "invalid"
    #         context['result'] = result    

    
    
    

