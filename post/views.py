from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Comment, Like
from .forms import PostForm, EditPostForm, AddCommentForm, AddReplyForm
from django.contrib import messages
from django.utils.text import slugify
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect


def all_posts(request):
    posts = Post.objects.all()
    for i in posts:
        print(i.plike.values("user_like"))
    return render(request, 'post/all_posts.html', {"posts": posts})


def post_detail(request, year, month, day, slug):
    post = get_object_or_404(Post, created__year=year, created__month=month, created__day=day, slug=slug)
    comments = Comment.objects.filter(post=post, is_reply=False)
    reply = AddReplyForm()
    can_like = False
    if request.user.is_authenticated:
        if post.user_can_like(request.user):
            can_like = True
    if request.method == "POST":
        form = AddCommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.user = request.user
            new_comment.post = post
            new_comment.save()
            messages.success(request, "Your comment submitted successfully!", 'success')
            return redirect("post:post_detail", year, month, day, slug)
    else:
        form = AddCommentForm()
    return render(request, 'post/post_detail.html',
                  {"post": post, "comments": comments, "form": form, "reply": reply, "can_like": can_like})


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
    else:
        return redirect("post:all_posts")


@login_required
def edit_post(request, user_id, post_id):
    if user_id == request.user.id:
        post = get_object_or_404(Post, pk=post_id)
        if request.method == "POST":
            form = PostForm(request.POST, instance=post)
            if form.is_valid():
                edited_post = form.save(commit=False)
                edited_post.user = request.user
                edited_post.slug = slugify(form.cleaned_data["body"][:30])
                edited_post.save()
                messages.success(request, "Your Post Edited", "success")
                return redirect("accounts:user_dashboard", user_id)

        else:
            form = EditPostForm(instance=post)
        return render(request, 'post/edit_post.html', {'form': form})

    else:
        return redirect("post:all_posts")


@login_required
def add_reply(request, post_id, comment_id):
    post = get_object_or_404(Post, id=post_id)
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.method == "POST":
        form = AddReplyForm(request.POST)
        if form.is_valid():
            new_reply = form.save(commit=False)
            new_reply.user = request.user
            new_reply.post = post
            new_reply.reply = comment
            new_reply.is_reply = True
            new_reply.save()
            messages.success(request, "Your reply submitted successfully!", 'success')
            return redirect("post:post_detail", post.created.year, post.created.month, post.created.day, post.slug)


@login_required
def like(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    like = Like(user_like=request.user, post_list=post)
    like.save()
    messages.success(request, "Liked!", 'success')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
