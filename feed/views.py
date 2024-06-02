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
from chat.models import ChatGroup
User = get_user_model()
# Create your views here.
from posts.models import Post,Comment,Report
from posts.forms import CommentForm

@login_required(login_url='/accounts/login/')
def feed_view(request):
    context = {}
    
    user = request.user
    try:
        user_profile = Profile.objects.get(user=user)
    except:
        return redirect('accounts:create_profile')
    try:
        user_skill = user_profile.skill.skill_name
    except:
        return redirect('accounts:create_profile')
    skill_group = ChatGroup.objects.filter(skill__skill_name=user_skill).first()
    is_participant = skill_group.participants.filter(id=user.id).exists() if skill_group else False
    
    context = {
        'is_participant': is_participant,
    }
    
    reported_posts = Report.objects.filter(reported_by=request.user).values_list('post_ref_id', flat=True)
    context['reported_posts'] = reported_posts
    posts_list = Post.objects.all()
    comments = Comment.objects.all()
    
    Comment_form = CommentForm()
    
    
    if request.method == 'POST':
        form = FeedPostForm(request.POST, request.FILES)
        if form.is_valid(): 
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
                      
                        print(f'Failed to send email to {follower.follower.email}: {e}')
                        messages.error(request, f'Post created but failed to send email to {follower.follower.username}: {e}')
                
        messages.success(request, 'Post created successfully!')
        return redirect('feed:feed')
    else:
        feed_post_form = FeedPostForm()

    context['feed_post_form'] = feed_post_form
    

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
            return redirect('feed:feed') 

    
    try:
        user_profile = Profile.objects.filter(user=request.user).first()
    except Profile.DoesNotExist:
        
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



 
    

