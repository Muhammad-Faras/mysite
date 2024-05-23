from django.urls import path
from .views import books_view


app_name = 'resources'
urlpatterns = [
    path('videos/', books_view, name='videos'),
]