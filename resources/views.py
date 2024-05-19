from django.shortcuts import render,HttpResponse
from .models import Books,VideosLinks
# Create your views here.


def books_view(request):
    context = {}
    books = Books.objects.all()
    context['books'] = books
    
    
    links = VideosLinks.objects.all()
    context['links'] = links
    return render(request, 'resources/books.html', context)