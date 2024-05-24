from django.urls import path
from .views import feed_view

app_name = 'feed'
urlpatterns = [
    path('', feed_view, name='feed'),
]