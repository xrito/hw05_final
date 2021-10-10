from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render

from .forms import PostForm, CommentForm
from .models import Group, Post, User, Comment, Follow


def index(request):
    search = request.GET.get('search', '')
    if search:
        post_list = Post.objects.filter(text__icontains=search)
    else:
        post_list = Post.objects.all()
    paginator = Paginator(post_list, settings.PAGE_POST)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'posts/index.html', context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    group_list = group.posts.all()
    paginator = Paginator(group_list, settings.PAGE_POST)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'group': group,
        'page_obj': page_obj,
    }
    return render(request, 'posts/group_list.html', context)


@login_required
def post_create(request):
    form = PostForm(request.POST or None,
                    files=request.FILES or None
                    )
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect('posts:profile', username=request.user)
    context = {
        'form': form,
    }
    return render(request, 'posts/create_post.html', context)


@login_required
def post_edit(request, post_id):
    post = get_object_or_404(Post, pk=post_id, author=request.user)
    form = PostForm(request.POST or None,
                    files=request.FILES or None,
                    instance=post
                    )
    if request.method == "POST":
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            return redirect('posts:post_detail', post_id=post_id)
    context = {
        'form': form,
        'post': post,
    }
    return render(request, 'posts/create_post.html', context)


def profile(request, username):
    user = get_object_or_404(User, username=username)
    posts = user.posts.all()
    paginator = Paginator(posts, settings.PAGE_POST)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    num_post = Post.objects.filter(author=user).count()
    following = Follow.objects.filter(author=user).exists()
    context = {
        'author': user,
        'page_obj': page_obj,
        'num_post': num_post,
        'following': following,
    }
    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    form = CommentForm(request.POST or None)
    comments = Comment.objects.filter(post=post_id)
    count = Post.objects.filter(author=post.author).count()
    context = {
        'post': post,
        'count': count,
        'form': form,
        'comments': comments,
    }
    return render(request, 'posts/post_detail.html', context)


@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
    return redirect('posts:post_detail', post_id=post_id)


@login_required
def follow_index(request):
    following = Follow.objects.filter(user=request.user).values('author')
    post_list = Post.objects.filter(author_id__in=following)
    paginator = Paginator(post_list, settings.PAGE_POST)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'posts/follow.html', context)


@login_required
def profile_follow(request, username):
    author = get_object_or_404(User, username=username)
    follow = Follow.objects.filter(
        user=request.user, author=author).exists()
    if follow or author == request.user:
        return redirect('posts:profile', username=request.user)
    Follow.objects.create(user=request.user, author=author)
    return redirect('posts:profile', username=author)


@login_required
def profile_unfollow(request, username):
    author = get_object_or_404(User, username=username)
    Follow.objects.filter(
        user=request.user, author=author).delete()
    return redirect('posts:profile', username=author)
