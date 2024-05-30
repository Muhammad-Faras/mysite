from django.urls import path
from .views import (
    create_post_view,
    update_post_view,
    detail_post_view,
    delete_post_view,
    my_posts_view,
    related_posts_view, 
    post_like_view,
    add_comment_view,
    report_post_view,
    add_to_wishlist,
    remove_from_wishlist,
    wishlist,
    ) 

app_name = 'posts'
urlpatterns = [
    path('create/', create_post_view, name='create-post'),
    path('update/<int:id>/', update_post_view, name='update-post'),
    path('detail/<int:id>/', detail_post_view, name='detail-post'),
    path('delete/<int:id>//confirm', delete_post_view, name='delete-post'),
    path('my-posts/', my_posts_view, name='my_posts'),
    path('related-posts/', related_posts_view, name='related_posts'),
    path('like-post/<int:pk>/', post_like_view, name='like_post'),
      path('add_comment/<int:post_id>/', add_comment_view, name='add_comment'),
    path('report/<int:post_id>/',report_post_view, name='report_post'),
    path('add_to_wishlist/<int:post_id>/', add_to_wishlist, name='add_to_wishlist'),
    path('remove_from_wishlist/<int:post_id>/', remove_from_wishlist, name='remove_from_wishlist'),
    path('wishlist/', wishlist, name='wishlist'),
    
]