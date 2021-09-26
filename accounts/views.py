from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import UserLoginForm, UserRegistrationForm
from django.contrib.auth.models import User
from post.models import Post


def user_login(request):
    if request.method == "POST":
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "Successfully Logged in", "success")
                return redirect("post:all_posts")
            else:
                messages.warning(request, "Wrong Username or Password", "warning")
                return redirect("accounts:user_login")
    else:
        form = UserLoginForm()
    return render(request, "accounts/login.html", {'form': form})


def user_register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password1']
            email = request.POST["email"]
            User.objects.create_user(username=username, password=password, email=email)
            messages.success(request, "You Registered Successfully", "success")
            return redirect("accounts:user_login")

    else:
        form = UserRegistrationForm()
    return render(request, "accounts/register.html", {'form': form})


def user_logout(request):
    logout(request)
    messages.success(request, "Successfully Logged out", "success")
    return redirect("accounts:user_login")


def user_dashboard(request, id):
    user = get_object_or_404(User, id=id)
    posts = Post.objects.filter(user=user)
    return render(request, 'accounts/dashboard.html', {'user': user, 'posts': posts})

