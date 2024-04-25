from django.shortcuts import render,HttpResponse

# Create your views here.
def project_view(request):
    return HttpResponse(request, 'project')