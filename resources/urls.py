from django.urls import path
from .views import books_view


app_name = 'resources'
urlpatterns = [
    path('', books_view, name='resources'),
]