from django.urls import path
from .views import (
    create_post_view,
    update_post_view,
    detail_post_view,
    delete_post_view,
    my_posts_view,
    related_posts_view, 
    post_like_view,
    ) 

app_name = 'posts'
urlpatterns = [
    path('create/', create_post_view, name='create-post'),
    path('update/<slug:slug>', update_post_view, name='update-post'),
    path('detail/<slug:slug>', detail_post_view, name='detail-post'),
    path('delete/<slug:slug>/confirm', delete_post_view, name='delete-post'),
    path('my-posts/', my_posts_view, name='my_posts'),
    path('related-posts/', related_posts_view, name='related_posts'),
    path('like-post/<int:pk>/', post_like_view, name='like_post')
    
]