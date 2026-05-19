from django.shortcuts import redirect, render

from assignments.models import About
from blogs.models import Blog, Category
from .forms import RegistrationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import auth


def home(request):
    featured_posts = Blog.objects.filter(is_featured=True).order_by("updated_at")
    posts = Blog.objects.filter(is_featured=False, status="Published")
    try:
        about = About.objects.get()
    except:
        about = None
    return render(
        request,
        "home.html",
        {
            "featured_posts": featured_posts,
            "posts": posts,
            "about": about,
        },
    )


def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("home")
        else:
            print(form.errors)
    else:
        form = RegistrationForm()
    return render(
        request,
        "register.html",
        {
            "form": form,
        },
    )


def login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            auth.login(request, form.get_user())  # 👈 One line, one source of truth
            return redirect("dashboard")
        print(form.errors)  # Move outside if-block
    else:
        form = AuthenticationForm()

    return render(request, "login.html", {"form": form})


def logout(request):
    auth.logout(request)
    return redirect("home")
