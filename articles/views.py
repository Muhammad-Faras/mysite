from django.shortcuts import render,HttpResponse,redirect,get_object_or_404
from .forms import ArticleForm
from .models import ArticleModel
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required(login_url='/accounts/login/')
def article_view(request):
    context = {}
    articles = ArticleModel.objects.all()
    context['articles'] = articles
    return render(request, 'articles/articles.html', context)


@login_required(login_url='/accounts/login/')
def publish_article(request):
    context = {}
    if request.method == 'POST':
        article_form = ArticleForm(request.POST, request.FILES)
        if article_form.is_valid():
            article = article_form.save(commit=False)
            article.author = request.user  
            article.save()
            return redirect('articles:articles')
        
    else:
        article_form = ArticleForm()
        
    context['article_form'] = article_form
    
    return render(request, 'articles/publish_article.html', context)
         
         
@login_required(login_url='/accounts/login/')
def article_detail(request,id):
    context = {}
    article = get_object_or_404(ArticleModel,pk=id)
    context['article'] = article
    
    return render(request, 'articles/article_detail.html', context)



@login_required(login_url='/accounts/login/')
def article_update(request, id):
    context = {}
    article = get_object_or_404(ArticleModel,pk=id)
    if request.user.is_authenticated:
        if request.method == 'POST':
            article_form = ArticleForm(request.POST,request.FILES, instance=article)
            if article_form.is_valid():
                article = article_form.save(commit=False)
                article.author = request.user  
                article.save() 
                return redirect('articles:articles')
            
        else:
            article_form = ArticleForm(instance=article)
        
    context['article_form'] = article_form
    context['article'] = article
    
    return render(request, 'articles/update_article.html', context)


@login_required(login_url='/accounts/login/')
def article_delete(request, id):
    context = {}
    article = get_object_or_404(ArticleModel,pk=id)
    if request.user == article.author:
        article.delete()
        context['article'] = article
        return redirect('articles:articles')
    


@login_required(login_url='/accounts/login/')
def related_articles_views(request):
    context = {}
    
    # Ensure the user is authenticated
    if request.user.is_authenticated:
        # Check if the user has a profile
        if hasattr(request.user, 'profile'):
            user_skill = request.user.profile.skill
            # Filter posts based on the user's skill
            related_articles = ArticleModel.objects.filter(author__profile__skill=user_skill)
            context['user_skill'] = user_skill
            context['related_articles'] = related_articles
        else:
            # Redirect to profile creation if the user doesn't have a profile
            return redirect('accounts:profile')
    else:
        # Handle the case where the user is not authenticated
        context['error'] = "User is not authenticated."
    
    
    return render(request, 'articles/related_articles.html', context)