from django.urls import path
from .views import article_view,article_detail, publish_article, article_update, article_delete, search_article_view


app_name = 'articles'
urlpatterns = [
    path('', article_view, name='articles'),
    path('publish/', publish_article, name='publish_article'),
    path('detail/<int:id>', article_detail, name='article_detail'),
    path('update/<int:id>', article_update, name='article_update'),
    path('delete/<int:id>', article_delete, name='article_delete'),
    path('delete/<int:id>', article_delete, name='article_delete'),
    path('search-articles/', search_article_view, name='search_articles'),
    
    
    
]