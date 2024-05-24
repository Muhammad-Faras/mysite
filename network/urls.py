from django.urls import path
from .views import network_view, search_users_view

app_name = 'network'
urlpatterns = [
    path('', network_view, name='network'),
    path('search/', search_users_view, name='search')
]