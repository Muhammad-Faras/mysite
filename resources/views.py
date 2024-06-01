from django.shortcuts import render,HttpResponse
from .models import Books,VideosLinks
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required(login_url='/accounts/login/')
def books_view(request):
    context = {}
    books = Books.objects.all()
    context['books'] = books
    
    return render(request, 'resources/books.html', context)