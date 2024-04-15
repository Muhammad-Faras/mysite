from django.shortcuts import render,redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from .forms import PostForm
from .models import Post
from django.shortcuts import get_object_or_404
from accounts.models import Profile
# Create your views here.

@login_required(login_url='/accounts/login/')
def create_post_view(request):
    context = {}
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)  # Ensure FILES are passed
        if form.is_valid():  # Correctly call is_valid() method
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('feed:feed')
    else:
        form = PostForm()
    
    context['form'] = form
    return render(request, 'posts/create_post.html', context)



def detail_post_view(request, slug):
    context = {}
    post = get_object_or_404(Post, slug=slug, author=request.user)
    context['post'] = post
    return render(request, 'posts/detail_post.html', context)


@login_required(login_url='/accounts/login/')
def update_post_view(request, slug):
    context = {}
    post = get_object_or_404(Post, slug=slug)
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = PostForm(request.POST, instance=post)
            if form.is_valid():
                form.save()
                return redirect('posts:detail-post', slug=slug)  # Redirect to the post detail page after successful update
        else:
            form = PostForm(instance=post)
        context['form'] = form  # Move this line inside the else block

    return render(request, 'posts/update_post.html', context)


@login_required(login_url='/accounts/login/')
def delete_post_view(request, slug):
    context = {}
    post = get_object_or_404(Post, slug=slug)
    
    if request.user.is_authenticated:
        if request.method == 'POST':
            post.delete()
            return redirect('feed:feed')  # Redirect to the post list page after successfully deleting the post
    context['post']= post
    return render(request, 'posts/delete_confirm_post.html', context)



# @login_required(login_url='/accounts/login/')
def my_posts_view(request):
    context = {}
    my_posts = Post.objects.filter(author=request.user)
    context['my_posts'] = my_posts
    return render(request, 'posts/my_posts.html', context)

def related_posts_view(request):
    context = {}
    
    # Ensure the user is authenticated
    if request.user.is_authenticated:
        # Access the profile attribute using lowercase 'profile'
        user_skill = request.user.profile.skill
        # Filter posts based on the user's skill
        related_posts = Post.objects.filter(author__profile__skill=user_skill)
        
        context['user_skill'] = user_skill
        context['related_posts'] = related_posts
    else:
        # Handle the case where the user is not authenticated
        context['error'] = "User is not authenticated."
    
    return render(request, 'posts/related_posts.html', context)
    
    
    
def post_like_view(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)

    return redirect('feed:feed')