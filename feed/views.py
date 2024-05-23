from django.shortcuts import render,redirect, HttpResponse,HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from accounts.models import Profile
from django.db.models import Q
from posts.forms import FeedPostForm
from django.contrib import messages
from accounts.models import Follow
from django.core.mail import send_mail
from django.urls import reverse

User = get_user_model()
# Create your views here.
from posts.models import Post,Comment
from posts.forms import CommentForm

@login_required(login_url='/accounts/login/')
def feed_view(request):
    context = {}
    context['id'] = request.user.id
    posts_list = Post.objects.all()
    comments = Comment.objects.all()
    
    Comment_form = CommentForm()
    
    
    if request.method == 'POST':
        form = FeedPostForm(request.POST, request.FILES)
        if form.is_valid():  # Correctly call is_valid() method
            post = form.save(commit=False)
            post.author = request.user
            post.save()

            post_url = request.build_absolute_uri(reverse('posts:detail-post', kwargs={'id': post.id}))
            followers = Follow.objects.filter(following=post.author)
            if followers.exists():
                for follower in followers:
                    try:
                        send_mail(
                            subject='Post Creation Notification',
                            message=f'Hi {follower.follower.username}, {post.author.username} has created a new post.You can view it here: {post_url}',
                            from_email='noorfaras809@gmail.com',
                            recipient_list=[follower.follower.email],
                        )
                    except Exception as e:
                        # Logging the error could be beneficial
                        print(f'Failed to send email to {follower.follower.email}: {e}')
                        messages.error(request, f'Post created but failed to send email to {follower.follower.username}: {e}')
                
        messages.success(request, 'Post created successfully!')
        return redirect('feed:feed')
    else:
        feed_post_form = FeedPostForm()

    context['feed_post_form'] = feed_post_form
    
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

    
    try:
        user_profile = Profile.objects.filter(user=request.user).first()
    except Profile.DoesNotExist:
        # Handle the case where the profile does not exist, if needed
        return redirect('accounts:profile',id)

    if user_profile:
        related_skill_users = Profile.objects.filter(skill=user_profile.skill).exclude(user=request.user).select_related('user')
        related_uni_users = Profile.objects.filter(university=user_profile.university).exclude(user=request.user).select_related('user')
        
        other_users = User.objects.exclude(
            Q(profile__skill=user_profile.skill) |
            Q(profile__university=user_profile.university) |
            Q(pk=request.user.pk)
        )
        
        context['related_skill_users'] = related_skill_users

    context['posts_list'] = posts_list
    
    context['comments'] = comments
    context['Comment_form'] = Comment_form
    return render(request, 'feed/feed.html', context)


@login_required(login_url='/accounts/login/')
def search_users_view(request):
    context = {}
    path_info = request.path_info
    print("Request Path:", path_info)

    if path_info.startswith('/network/'):
        context = {}
    path_info = request.path_info
    print("Request Path:", path_info)

    if path_info.startswith('/network/'):
        print("In Network Condition")
        if request.method == 'POST':
            search_query = request.POST.get('search-query')
            search_result = User.objects.filter(username__icontains=search_query) | User.objects.filter(email__icontains=search_query)
            context['search_result'] = search_result
            print("Network search results:", search_result)  # Debugging info
            return render(request, 'network/search.html', context)
        else:
            return redirect('network:network')

    elif path_info.startswith('/feed/'):
        print("In Feed Condition")
        if request.method == 'POST':
            search_query = request.POST.get('search-query')
            search_result = Post.objects.filter(title__icontains=search_query)
            context['search_result'] = search_result
            print("Feed search results:", search_result)  # Debugging info
            return render(request, 'feed/search.html', context)
        else:
            return redirect('feed:feed')

    else:
        print("Unhandled Request Path:", path_info)
        return HttpResponse('Page Not Found')
    
    

