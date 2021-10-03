from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import UserLoginForm, UserRegistrationForm, ProfileForm, EmailLoginForm, VerifyCodeForm, ChangePasswordForm
from django.contrib.auth.models import User
from post.models import Post
from django.contrib.auth.decorators import login_required
from random import randint
from kavenegar import *
from .models import Relations
from django.http import JsonResponse


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
    is_following = False
    self_dash = False
    relation = Relations.objects.filter(from_user=request.user, to_user=user)
    if relation.exists():
        is_following = True
    if request.user.id == user.id:
        self_dash = True
    return render(request, 'accounts/dashboard.html', {'user': user, 'posts': posts,
                                                       'self_dash': self_dash, 'is_following': is_following})


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


def email_login(request):
    if request.method == "POST":
        form = EmailLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            rand_num = randint(1000, 9999)
            api = KavenegarAPI(
                '747047636F634A774D683877706968445A38664D64415166796779394546507272424B4C76534A456248513D')
            params = {'sender': '', 'receptor': '09353098300', 'message': rand_num}
            api.sms_send(params)
            return redirect("accounts:verify", email, rand_num)
    else:
        form = EmailLoginForm()
    return render(request, 'accounts/email_login.html', {"form": form})


def verify(request, user_email, rand_num):
    if request.method == "POST":
        form = VerifyCodeForm(request.POST)
        if form.is_valid():
            user = get_object_or_404(User, email=user_email)
            if rand_num == form.cleaned_data['code']:
                login(request, user)
                messages.success(request, "successfully logged in", 'success')
                return redirect("post:all_posts")
            else:
                messages.warning(request, "code is wrong!", 'warning')
    else:
        form = VerifyCodeForm()
    return render(request, 'accounts/verify.html', {"form": form})


@login_required
def follow(request):
    if request.method == 'POST':
        user_id = request.POST['user_id']
        following = get_object_or_404(User, pk=user_id)
        check_relation = Relations.objects.filter(from_user=request.user, to_user=following)
        if check_relation.exists():
            return JsonResponse({'status': 'exists'})
        else:
            Relations(from_user=request.user, to_user=following).save()
            return JsonResponse({'status': 'ok'})


@login_required
def unfollow(request):
    if request.method == 'POST':
        user_id = request.POST['user_id']
        following = get_object_or_404(User, pk=user_id)
        check_relation = Relations.objects.filter(from_user=request.user, to_user=following)
        if check_relation.exists():
            check_relation.delete()
            return JsonResponse({'status': 'ok'})
        else:
            return JsonResponse({'status': 'notexists'})


@login_required
def change_password(request, user_id):
    if request.method == "POST":

        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            user = get_object_or_404(User, id=user_id)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            messages.success(request, "password changed successfully!", "success")
            return redirect("accounts:user_login")
    else:
        form = ChangePasswordForm()

    return render(request, "accounts/change_password.html", {"form": form})
