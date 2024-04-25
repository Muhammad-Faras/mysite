from django.shortcuts import render,HttpResponse,redirect,get_object_or_404
from .forms import ArticleForm
from .models import ArticleModel
# Create your views here.
def article_view(request):
    context = {}
    articles = ArticleModel.objects.all()
    context['articles'] = articles
    return render(request, 'articles/articles.html', context)


def publish_article(request):
    context = {}
    if request.method == 'POST':
        article_form = ArticleForm(request.POST)
        if article_form.is_valid():
            article = article_form.save(commit=False)
            article.author = request.user  
            article.save() 
            return redirect('articles:articles')
        else:
            article_form = ArticleForm()
    else:
        article_form = ArticleForm()
        
    context['article_form'] = article_form
    
    return render(request, 'articles/publish_article.html', context)
         

def article_detail(request,id):
    context = {}
    article = get_object_or_404(ArticleModel,pk=id)
    context['article'] = article
    
    return render(request, 'articles/article_detail.html', context)




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

def article_delete(request, id):
    context = {}
    article = get_object_or_404(ArticleModel,pk=id)
    if request.user == article.author:
        article.delete()
        context['article'] = article
        return redirect('articles:articles')
    