from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import UserLoginForm, UserRegistrationForm, ProfileForm
from django.contrib.auth.models import User
from post.models import Post
from django.contrib.auth.decorators import login_required
from .models import Profile


def user_login(request):
    next = request.GET.get("next")
    print(next)
    if request.method == "POST":
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "Successfully Logged in", "success")
                if next:
                    return redirect(next)
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


@login_required
def user_logout(request):
    logout(request)
    messages.success(request, "Successfully Logged out", "success")
    return redirect("accounts:user_login")


@login_required
def user_dashboard(request, id):
    user = get_object_or_404(User, id=id)
    posts = Post.objects.filter(user=user)
    self_dash = False
    if request.user.id == user.id:
        self_dash = True
    return render(request, 'accounts/dashboard.html', {'user': user, 'posts': posts, 'self_dash': self_dash})


@login_required
def edit_profile(request, user_id):
    if request.user.id == user_id:
        initial = {
            'email': request.user.email,
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
        }
        user = get_object_or_404(User, id=user_id)
        if request.method == "POST":
            form = ProfileForm(request.POST, instance=user.profile, initial=initial)
            if form.is_valid():
                form.save()
                user.email = form.cleaned_data['email']
                user.first_name = form.cleaned_data['first_name']
                user.last_name = form.cleaned_data['last_name']
                user.save()
                messages.success(request, "Your Profile Edited Successfully!", 'success')
                return redirect("accounts:user_dashboard", user_id)
        else:
            form = ProfileForm(instance=user.profile, initial=initial)
        return render(request, "accounts/edit_profile.html", {"form": form})
