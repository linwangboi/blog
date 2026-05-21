from django.shortcuts import get_object_or_404, redirect, render

from blogs.models import Blog, Category
from django.contrib.auth.decorators import login_required

from .forms import CategoryForm


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
