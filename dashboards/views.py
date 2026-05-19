from django.shortcuts import render

from blogs.models import Blog, Category
from django.contrib.auth.decorators import login_required


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
