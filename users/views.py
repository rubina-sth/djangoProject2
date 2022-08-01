from multiprocessing import context
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from .models import Profile
from .forms import CustomUserCreationForm, ProfileForm, SkillForm


def profiles(request):
    if request.GET.get('search_query'):
        search_query = request.GET['search_query']
        profiles = Profile.objects.filter(name__iexact=search_query)
    else:
        profiles = Profile.objects.all()
    context = {
        'profiles': profiles
    }
    return render(request, 'users/profiles.html', context)


def profile(request, pk):
    profile = Profile.objects.get(id=pk)
    describedSkill = profile.skill_set.exclude(description__exact="")
    otherSkill = profile.skill_set.filter(description__exact="")
    context = {
        'profile': profile,
        'describedSkill': describedSkill,
        'otherSkill': otherSkill
    }
    return render(request, 'users/user_profile.html', context)

def registerUser(request):
    page = 'register'
    form = CustomUserCreationForm()
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            messages.success(request, 'Account created succesfully')
            login(request, user)
            return redirect('edit-profile')
        else:
            messages.error(request, 'An error occurred')
    context = {
        'page': page,
        'form': form
    }
    return render(request, 'users/login_register.html', context)

def loginUser(request):
    if request.user.is_authenticated:
        return redirect('profiles')

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        try:
            user = Profile.objects.get(username=username)
        except:
            messages.error(request, 'Username does not exist!')

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('profiles')
        else:
            messages.error(request, 'Username or Password does not match!')
    return render(request, 'users/login_register.html')

@login_required(login_url='login')
def account(request):
    profile = request.user.profile
    skills = profile.skill_set.all()
    projects = profile.project_set.all()
    context = {
        'profile': profile,
        'skills': skills,
        'projects': projects
    }
    return render(request, 'users/account.html', context)

@login_required(login_url='login')
def editProfile(request):
    profile = request.user.profile
    form = ProfileForm(instance=profile)
    context = {
        'form': form
    }
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile Updated Successfully!')
            return redirect('account')

    return render(request, 'users/profile_form.html', context)

@login_required(login_url='login')
def addSkill(request):
    page = 'Add'
    profile = request.user.profile
    form = SkillForm()
    context = {
        'form': form,
        'page': page
    }
    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.owner = profile
            skill.save()
            messages.success(request, f"'{skill.name}' added successfully!")
            return redirect('account')

    return render(request, 'users/skill_form.html', context)

@login_required(login_url='login')
def editSkill(request, pk):
    page = 'Update'
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    form = SkillForm(instance=skill)
    if request.method == 'POST':
        form = SkillForm(request.POST, instance=skill)
        if form.is_valid():
            form.save()
            messages.success(request, 'Skill updated')
            return redirect('account')
    context = {
        'form': form,
        'page': page
    }
    return render(request, 'users/skill_form.html', context)

def deleteSkill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    context = {
        'obj': skill
    }
    if request.method == 'POST':
        skill.delete()
        return redirect('account')
    return render(request, 'partials/_delete_form.html', context)


def logoutUser(request):
    logout(request)
    return redirect('login')
