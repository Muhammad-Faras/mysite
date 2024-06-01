from django.urls import path
from .views import (
 
    update_post_view,
    detail_post_view,
    delete_post_view,

    related_posts_view, 
    post_like_view,
    add_comment_view,
    report_post_view,
   
    ) 

app_name = 'posts'
urlpatterns = [
 
    path('update/<int:id>/', update_post_view, name='update-post'),
    path('detail/<int:id>/', detail_post_view, name='detail-post'),
    path('delete/<int:id>//confirm', delete_post_view, name='delete-post'),
   
    path('related-posts/', related_posts_view, name='related_posts'),
    path('like-post/<int:pk>/', post_like_view, name='like_post'),
    path('add_comment/<int:post_id>/', add_comment_view, name='add_comment'),
    path('report/<int:post_id>/',report_post_view, name='report_post'),
   
    
]