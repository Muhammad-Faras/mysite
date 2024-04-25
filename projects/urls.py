from django.urls import path
from .views import project_view


app_name = 'projects'
urlpatterns = [
    path('', project_view, name='projects'),
]