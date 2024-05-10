from django.urls import path
from .views import network_view

app_name = 'network'
urlpatterns = [
    path('', network_view, name='network')
]