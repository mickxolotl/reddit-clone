from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import RedditUserCreationForm, AuthForm, EditProfileForm
from django.contrib.auth import login, logout, get_user
from django.contrib import messages
from django.core.paginator import Paginator
from django.views.generic import ListView
from . import models


class PostListView(ListView):
    model = models.Post
    template_name = 'rddt_main/main.html'
    context_object_name = "post_list"
    paginate_by = 10


def register(request):
    if request.user.is_authenticated:
        return redirect('rddt_main:profile')

    if request.method == 'POST':
        form = RedditUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('rddt_main:profile')
    else:
        form = RedditUserCreationForm()

    return render(request, 'rddt_main/register.html', context={"form": form})


def login_page(request):
    if request.user.is_authenticated:
        return redirect('rddt_main:homepage')

    if request.method == 'POST':
        form = AuthForm(data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('rddt_main:homepage')
    else:
        form = AuthForm

    return render(request, 'rddt_main/login.html', context={"form": form})


def logout_page(request):
    logout(request)
    return redirect('rddt_main:homepage')


def profile(request):
    if not request.user.is_authenticated:
        return redirect('rddt_main:login')
    user = get_user(request)

    if request.method == 'POST':
        form = EditProfileForm(data=request.POST, instance=user)

        if form.is_valid():
            form.save()
            messages.success(request, 'Изменения сохранены')
            return redirect('rddt_main:profile')
    else:
        form = EditProfileForm(instance=user)

    return render(request, 'rddt_main/profile.html', context={"form": form})
