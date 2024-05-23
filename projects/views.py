from django.shortcuts import render,redirect,get_object_or_404,HttpResponse
from .models import ProjcetShowcase
from .forms import ProjcetShowcase_Form
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required(login_url='/accounts/login/')
def project_view(request):
    context={}
    projects = ProjcetShowcase.objects.all()
    context['projects'] = projects
    return render(request, 'projects/projects.html', context)

@login_required(login_url='/accounts/login/')
def create_project_view(request):
    context={}
    form = ProjcetShowcase_Form()
    if request.method == 'POST':
        form = ProjcetShowcase_Form(request.POST, request.FILES)
        if request.user.is_authenticated:
            if form.is_valid():
                project = form.save(commit=False)
                project.author = request.user
                project.save()
                return redirect('projects:projects')
            else:
                form = ProjcetShowcase_Form()
        else:
            return redirect('accounts_login')
    else:
        form = ProjcetShowcase_Form()
    context['form'] = form
    return render(request, 'projects/create_project.html', context)


@login_required(login_url='/accounts/login/')
def project_detail_view(request, id):
    context = {}
    project = get_object_or_404(ProjcetShowcase, pk=id)
    context['project'] = project
    return render(request, 'projects/project_detail.html', context)

@login_required(login_url='/accounts/login/')
def project_update_view(request, id):
    context={}
    project = get_object_or_404(ProjcetShowcase, pk=id)
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = ProjcetShowcase_Form(request.POST, request.FILES,instance=project)
            if form.is_valid():
                project = form.save(commit=False)
                project.author = request.user
                project.save()
                return redirect('projects:projects')
        else:
            form = ProjcetShowcase_Form(instance=project)
    else:
        return redirect('accounts_login')

    context['form'] = form
    context['project'] = project
    return render(request, 'projects/project_update.html', context)
    
@login_required(login_url='/accounts/login/')
def project_delete_view(request, id):
    project = get_object_or_404(ProjcetShowcase, pk=id)
    if request.user.is_authenticated:
        project.delete()
        return redirect('projects:projects')
    