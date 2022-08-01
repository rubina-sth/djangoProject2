from django import forms
from django.shortcuts import redirect, render
from django.http import HttpResponse
from .models import Project
from .forms import ProjectForm
from django.contrib.auth.decorators import login_required


def projects(request):
    projects = Project.objects.all()
    context = {
        'projects': projects,
    }
    return render(request, 'projects/projects.html', context)


def project(request, pk):
    singleProject = Project.objects.get(id=pk)
    tags = singleProject.tags.all()
    context = {
        'project': singleProject,
        'tags': tags
    }
    return render(request, 'projects/single_project.html', context)

@login_required(login_url='login')
def addProject(request):
    page = 'Add'
    form = ProjectForm()
    profile = request.user.profile
    context = {
        'form': form,
        'page': page
    }
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = profile
            project.save()
            return redirect('account')
    return render(request, 'projects/project_form.html', context)

@login_required(login_url='login')
def editProject(request, pk):
    page = 'Update'
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    form = ProjectForm(instance=project)
    context = {
        'form': form,
        'page': page
    }

    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            return redirect('account')
    return render(request, 'projects/project_form.html', context)

@login_required(login_url='login')
def deleteProject(request, pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    context = {
        'obj': project
    }
    if request.method == 'POST':
        project.delete()
        return redirect('account')

    return render(request, 'partials/_delete_form.html', context)
