from django.shortcuts import render, redirect, get_object_or_404
from .forms import RedditUserCreationForm, AuthForm, EditProfileForm, NewPostForm, CommentForm
from django.contrib.auth import login, logout, get_user
from django.contrib import messages
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


def create_post(request):
    if not request.user.is_authenticated:
        return redirect('rddt_main:login')
    # user = get_user(request)

    if request.method == 'POST':
        form = NewPostForm(data=request.POST)

        if form.is_valid():
            post = form.save(False)
            post.author = request.user
            post.save()
            messages.success(request, 'Пост опубликован')
            return redirect('rddt_main:homepage')
    else:
        form = NewPostForm()

    return render(request, 'rddt_main/create_post.html', context={"form": form})


def post_page(request, post_id):
    post = get_object_or_404(models.Post, pk=post_id)
    return render(request, 'rddt_main/post.html', context={
        "post": post,
        'comment_form': CommentForm()
    })


def post_comment(request, post_id):
    if not request.user.is_authenticated:
        return redirect('rddt_main:login')

    if request.method == 'POST':
        post = get_object_or_404(models.Post, pk=post_id)
        form = CommentForm(data=request.POST)

        if form.is_valid():
            comment = form.save(False)
            comment.author = request.user
            comment.replied_post = post
            comment.save()
            messages.success(request, 'Комментарий опубликован')
        else:
            messages.error(request, 'Ошибка при публикации комментария')

    return redirect('rddt_main:post', post_id)


def comment_reply(request, post_id):
    post = get_object_or_404(models.Post, pk=post_id)

    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('rddt_main:login')

        form = CommentForm(data=request.POST)

        if form.is_valid():
            comment = form.save(False)
            comment.author = request.user
            comment.replied_post = post
            comment.save()
            messages.success(request, 'Комментарий опубликован')
        else:
            messages.error(request, 'Ошибка при публикации комментария\n%s' % form.errors)

        return redirect('rddt_main:post', post_id)

    else:
        data = request.GET.dict()
        form = CommentForm(initial=data)
        if data.get('nojs', 0) == '1':
            return render(request, 'rddt_main/reply_form_full.html', context={'comment_form': form})

        return render(request, 'rddt_main/reply_form_snippet.html', context={'comment_form': form, 'post': post})
