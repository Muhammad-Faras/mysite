from django.shortcuts import render,redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from .forms import PostForm,CommentForm
from .models import Post,Comment
from django.shortcuts import get_object_or_404
from accounts.models import Profile
from django.contrib.auth import get_user_model
from django.http import JsonResponse
# Create your views here.
User = get_user_model()

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



def detail_post_view(request, id):
    context = {}
    comments = Comment.objects.all()
    
    Comment_form = CommentForm()
# Inside your view function
    if request.method == 'POST':
        Comment_form = CommentForm(request.POST)
        if Comment_form.is_valid():
            post_id = request.POST.get('post_id')
            print('post ki id ya ha = ',post_id)
            post = Post.objects.get(pk=id)
            comment = Comment_form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            Comment_form = CommentForm()
            
    post = get_object_or_404(Post, pk=id)
    context['post'] = post
    context['comments'] = comments
    context['comment_form'] = Comment_form
    return render(request, 'posts/detail_post.html', context)


@login_required(login_url='/accounts/login/')
def update_post_view(request, id):
    context = {}
    post = get_object_or_404(Post, pk=id)
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = PostForm(request.POST, instance=post)
            if form.is_valid():
                form.save()
                return redirect('posts:detail-post', id=id)  # Redirect to the post detail page after successful update
        else:
            form = PostForm(instance=post)
        context['form'] = form  # Move this line inside the else block

    return render(request, 'posts/update_post.html', context)


@login_required(login_url='/accounts/login/')
def delete_post_view(request, id):
    context = {}
    post = get_object_or_404(Post, pk=id)
    
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
        # Check if the user has a profile
        if hasattr(request.user, 'profile'):
            # Access the profile attribute
            user_skill = request.user.profile.skill
            # Filter posts based on the user's skill
            related_posts = Post.objects.filter(author__profile__skill=user_skill)
            
            context['user_skill'] = user_skill
            context['related_posts'] = related_posts
        else:
            # Redirect to profile creation if the user doesn't have a profile
            return redirect('accounts:profile')
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


def add_to_wishlist(request, post_id):
    post = Post.objects.get(id=post_id)
    post.wishlist = True
    post.save()
    return redirect('feed:feed',)

def remove_from_wishlist(request, post_id):
    post = Post.objects.get(id=post_id)
    post.wishlist = False
    post.save()
    return redirect('feed:feed')

def wishlist(request):
    wishlist_posts = Post.objects.filter(wishlist=True)
    return render(request, 'posts/wishlist.html', {'wishlist_posts': wishlist_posts})
