from django.shortcuts import render, get_object_or_404, redirect
from .models import Post
from .forms import PostForm
from django.contrib import messages
from django.utils.text import slugify
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


def all_posts(request):
    posts = Post.objects.all()
    return render(request, 'post/all_posts.html', {"posts": posts})


def post_detail(request, year, month, day, slug):
    post = get_object_or_404(Post, created__year=year, created__month=month, created__day=day, slug=slug)
    return render(request, 'post/post_detail.html', {"post": post})


@login_required
def add_post(request, id):
    if request.user.id == id:
        if request.method == "POST":
            form = PostForm(request.POST)
            if form.is_valid():
                new_post = form.save(commit=False)
                new_post.user = request.user
                new_post.slug = slugify(form.cleaned_data["body"][:30])
                new_post.save()
                messages.success(request, "Your Post Submitted", "success")
                return redirect("accounts:user_dashboard", id)

        else:
            form = PostForm()
        return render(request, 'post/add_post.html', {"form": form})
    else:
        return redirect("post:all_posts")


@login_required
def delete_post(request, user_id, post_id):
    if user_id == request.user.id:
        user = get_object_or_404(User, id=user_id)
        post = get_object_or_404(Post, user=user, id=post_id)
        post.delete()
        messages.success(request, "Your Post Deleted Successfully!", "success")
        return redirect("accounts:user_dashboard", user_id)
    else :
        return redirect("post:all_posts")
