from django.shortcuts import render,HttpResponse
from .models import Books
# Create your views here.


def books_view(request):
    context = {}
    books = Books.objects.all()
    context['books'] = books
    return render(request, 'resources/books.html', context)