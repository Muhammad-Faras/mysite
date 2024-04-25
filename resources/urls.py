from django.urls import path
from .views import resource_view


app_name = 'resources'
urlpatterns = [
    path('', resource_view, name='resources'),
]