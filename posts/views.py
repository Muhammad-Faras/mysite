from django.shortcuts import render,redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from .forms import CommentForm,ReportForm,FeedPostForm
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

from .models import Post


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
            form = FeedPostForm(request.POST, request.FILES, instance=post)
            if form.is_valid():
                form.save()
                messages.info(request,'updated successfully')
                return redirect('posts:detail-post', id=id)  
        else:
            form = FeedPostForm(instance=post)
        context['form'] = form 

    return render(request, 'posts/update_post.html', context)


@login_required(login_url='/accounts/login/')
def delete_post_view(request, id):
    context = {}
    post = get_object_or_404(Post, pk=id)
    
    if request.user.is_authenticated:
        if request.method == 'POST':
            post.delete()
            messages.info(request,'post deleted successfully')
            return redirect('feed:feed')  
    context['post']= post
    return render(request, 'posts/delete_confirm_post.html', context)






def related_posts_view(request):
    context = {}
    
    try:
        if request.user.profile.is_complete():
            if request.user.is_authenticated:
                if hasattr(request.user, 'profile'):
                    user_skill = request.user.profile.skill
                    related_posts = Post.objects.filter(author__profile__skill=user_skill)
                    
                    context['user_skill'] = user_skill
                    context['related_posts'] = related_posts
                
                else:
                    return redirect('accounts:create_profile')
            else:
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
    




from django.core.exceptions import ObjectDoesNotExist
@login_required
def report_post_view(request, post_id):
    context={}
    post = get_object_or_404(Post, id=post_id)
    
    try:
       
        existing_report = Report.objects.get(post_ref=post, reported_by=request.user)
        if existing_report:
            messages.success(request, 'Already reported')
            return redirect('feed:feed')
    except ObjectDoesNotExist:
       
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