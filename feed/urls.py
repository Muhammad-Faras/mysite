from django.urls import path
from .views import feed_view, search_users_view

app_name = 'feed'
urlpatterns = [
    path('', feed_view, name='feed'),
    path('users/', search_users_view, name='search-users')
]