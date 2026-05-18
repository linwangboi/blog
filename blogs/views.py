from django.shortcuts import get_object_or_404, render
from django.db.models import Q

from .models import Blog, Category


def posts_by_category(request, category_id):
    posts = Blog.objects.filter(status="Published", category=category_id)
    category = get_object_or_404(Category, pk=category_id)
    return render(
        request,
        "posts_by_category.html",
        {
            "posts": posts,
            "category": category,
        },
    )


def blogs(request, slug):
    single_blog = get_object_or_404(Blog, slug=slug, status="Published")

    return render(
        request,
        "blogs.html",
        {
            "single_blog": single_blog,
        },
    )


def search(request):
    keyword = request.GET.get("keyword")

    return render(
        request,
        "search.html",
        {
            "blogs": Blog.objects.filter(
                Q(title__icontains=keyword) | Q(blog_body__icontains=keyword)
            ),
            'keyword': keyword or '',
        },
    )
