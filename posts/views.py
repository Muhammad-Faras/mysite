from django.shortcuts import render,redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from .forms import PostForm,CommentForm,ReportForm
from .models import Post,Comment,Report
from django.shortcuts import get_object_or_404
from accounts.models import Profile
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.contrib import messages
from accounts.models import Follow
from django.core.mail import send_mail
# Create your views here.
User = get_user_model()

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib import messages
from .forms import PostForm
from .models import Post


@login_required(login_url='/accounts/login/')
def create_post_view(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            print('-----------',post.author)
            # Check if the current user is following the post author
            followers = Follow.objects.filter(following=post.author)
            if followers:
                print('Followers of the post author:', followers)
            else:
                print('------------------------------------------',)
                
            for follower in followers:
                print('Current follower being checked:', follower.follower)
                if follower.follower == request.user:
                    try:
                        send_mail(
                            subject='Post Creation Notification',
                            message=f'Hi {request.user.username}, {post.author.username} has created a new post.',
                            from_email='noorfaras809@gmail.com',
                            recipient_list=[request.user.email],
                        )
                        messages.success(request, 'Post created successfully and notification sent!')
                    except Exception as e:
                        messages.error(request, f'Post created but failed to send email: {e}')
                    break  # No need to check other followers once we find the current user
            else:
                messages.success(request, 'Post created successfully!')

            return redirect('accounts:profile', id=post.author.id)
        else:
            messages.error(request, 'Failed to create post. Please correct the errors below.')

    else:
        form = PostForm()

    context = {'form': form}
    return render(request, 'posts/create_post.html', context)


@login_required(login_url='/accounts/login/')
def detail_post_view(request, id):
    context = {}
    post = get_object_or_404(Post, pk=id)
    comments = Comment.objects.filter(post=post)
    comment_form = CommentForm()

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            messages.success(request, 'Comment successfully posted')
            return redirect('posts:detail-post', id=id)
        else:
            messages.error(request, 'There was an error posting your comment. Please try again.')

    context['post'] = post
    context['comment_form'] = comment_form
    context['comments'] = comments

    return render(request, 'posts/detail_post.html', context)


@login_required(login_url='/accounts/login/')
def update_post_view(request, id):
    context = {}
    post = get_object_or_404(Post, pk=id)
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = PostForm(request.POST, request.FILES, instance=post)
            if form.is_valid():
                form.save()
                messages.info(request,'updated successfully')
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
            messages.info(request,'post deleted successfully')
            return redirect('feed:feed')  # Redirect to the post list page after successfully deleting the post
    context['post']= post
    return render(request, 'posts/delete_confirm_post.html', context)



# @login_required(login_url='/accounts/login/')
@login_required(login_url='/accounts/login/')
def my_posts_view(request):
    context = {}
    my_posts = Post.objects.filter(author=request.user)
    context['my_posts'] = my_posts
    return render(request, 'posts/my_posts.html', context)

def related_posts_view(request):
    context = {}
    
    try:
        if request.user.profile.is_complete():
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
                    return redirect('accounts:create_profile')
            else:
                # Handle the case where the user is not authenticated
                context['error'] = "User is not authenticated."
        
        return render(request, 'posts/related_posts.html', context)
    
    except:
        messages.info(request, 'complete your profile for related posts')
        return redirect('accounts:create_profile')
        
    
from django.http import JsonResponse
@login_required(login_url='/accounts/login/')
def post_like_view(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True
    return JsonResponse({'liked': liked, 'like_count': post.likes.count()})

@login_required
def add_comment_view(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    
    if request.method == 'POST':
        comment_body = request.POST.get('comment_body')
        if comment_body:
            comment = Comment.objects.create(post=post, author=request.user, comment_body=comment_body)
            response_data = {
                'success': True,
                'username': request.user.username,
                'comment_body': comment.comment_body
            }
            return JsonResponse(response_data)
    return JsonResponse({'success': False})
    

@login_required(login_url='/accounts/login/')
def add_to_wishlist(request, post_id):
    post = Post.objects.get(id=post_id)
    post.wishlist = True
    post.save()
    return redirect('feed:feed',)

@login_required(login_url='/accounts/login/')
def remove_from_wishlist(request, post_id):
    post = Post.objects.get(id=post_id)
    post.wishlist = False
    post.save()
    return redirect('feed:feed')

@login_required(login_url='/accounts/login/')
def wishlist(request):
    wishlist_posts = Post.objects.filter(wishlist=True)
    return render(request, 'posts/wishlist.html', {'wishlist_posts': wishlist_posts})


from django.core.exceptions import ObjectDoesNotExist
@login_required
def report_post_view(request, post_id):
    context={}
    post = get_object_or_404(Post, id=post_id)
    
    try:
        # Check if the user has already reported this post
        existing_report = Report.objects.get(post_ref=post, reported_by=request.user)
        if existing_report:
            existing_report.delete()
            messages.success(request, 'Report removed successfully.')
            return redirect('feed:feed')
    except ObjectDoesNotExist:
        # No report exists, proceed with form handling
        if request.method == 'POST':
            form = ReportForm(request.POST, request.FILES)
            if form.is_valid():
                report = form.save(commit=False)
                report.post_ref = post
                report.reported_by = request.user
                report.save()
                messages.success(request, 'Report submitted successfully.')
                return redirect('feed:feed')
        else:
            form = ReportForm()

    context['post'] = post
    context['form'] = form
    return render(request, 'posts/report_post.html', context)