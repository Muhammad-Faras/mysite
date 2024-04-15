from django.urls import path
from .views import feed_view

app_name = 'network'
urlpatterns = [
    path('', feed_view, name='network')
]