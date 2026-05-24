from django.shortcuts import get_object_or_404, redirect, render

from blogs.models import Blog, Category
from django.contrib.auth.decorators import login_required

from .forms import AddUserForm, BlogPostForm, CategoryForm
from django.template.defaultfilters import slugify
from django.contrib.auth import get_user_model


@login_required(login_url="login")
def dashboard(request):
    blogs_count = Blog.objects.count()
    category_count = Category.objects.count()
    return render(
        request,
        "dashboard/dashboard.html",
        {
            "blogs_count": blogs_count,
            "category_count": category_count,
        },
    )


@login_required(login_url="login")
def categories(request):
    return render(request, "dashboard/categories.html")


@login_required(login_url="login")
def add_category(request):
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("categories")
    form = CategoryForm()
    return render(
        request,
        "dashboard/add_category.html",
        {
            "form": form,
        },
    )


def edit_category(request, pk):
    cat = get_object_or_404(Category, pk=pk)
    if request.method == "GET":
        form = CategoryForm(instance=cat)
    elif request.method == "POST":
        form = CategoryForm(instance=cat, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect("categories")
    return render(
        request,
        "dashboard/edit_category.html",
        {"form": form, "cat": cat},
    )


def delete_category(request, pk):
    cat = get_object_or_404(Category, pk=pk)
    cat.delete()
    return redirect("categories")


def posts(request):
    posts = Blog.objects.all().order_by("-created_at")

    return render(request, "dashboard/posts.html", {"posts": posts})


def add_post(request):
    if request.method == "POST":
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            post.slug = f"{slugify(post.title)}-{post.id}"  #!!!!
            post.save()
            return redirect("posts")

    form = BlogPostForm()
    return render(
        request,
        "dashboard/add_post.html",
        {
            "form": form,
        },
    )


def edit_post(request, pk):
    post = get_object_or_404(Blog, pk=pk)
    if request.method == "POST":
        form = BlogPostForm(data=request.POST, files=request.FILES, instance=post)
        if form.is_valid():
            post = form.save()
            if post.title != form.cleaned_data["title"]:
                post.slug = f"{slugify(post.title)-{post.id}}"
                post.save()
            return redirect("posts")

    form = BlogPostForm(instance=post)
    return render(
        request,
        "dashboard/edit_post.html",
        {
            "form": form,
            "post": post,
        },
    )


def delete_post(request, pk):
    post = get_object_or_404(Blog, pk=pk)
    post.delete()
    return redirect("posts")


def users(request):
    users = get_user_model().objects.all()
    return render(
        request,
        "dashboard/users.html",
        {
            "users": users,
        },
    )


def add_user(request):
    if request.method == "POST":
        form = AddUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("users")

    form = AddUserForm()
    return render(
        request,
        "dashboard/add_user.html",
        {
            "form": form,
        },
    )


def edit_user(request, pk):
    user = get_object_or_404(get_user_model(), pk=pk)
    if request.method == "POST":
        form = AddUserForm(instance=user, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect("users")
        print(form.errors)
    form = AddUserForm(instance=user)
    return render(request, "dashboard/edit_user.html", {"user": user, "form": form})


def delete_user(request, pk):
    user = get_object_or_404(get_user_model(), pk=pk)
    user.delete()
    return redirect("users")
