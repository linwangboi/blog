from django.shortcuts import get_object_or_404, redirect, render
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from .models import Blog, Category, Comment


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
    comments = Comment.objects.filter(blog=single_blog)

    return render(
        request,
        "blogs.html",
        {
            "single_blog": single_blog,
            "comments": comments,
            "comment_count": comments.count(),
        },
    )


@login_required(login_url="login")
def add_comment(request, slug):
    user = request.user
    blog = get_object_or_404(Blog, slug=slug, status="Published")
    comment = request.POST.get("comment")
    Comment.objects.create(user=user, blog=blog, comment=comment)
    return redirect("blogs", slug=slug)


def search(request):
    keyword = request.GET.get("keyword")

    return render(
        request,
        "search.html",
        {
            "blogs": Blog.objects.filter(
                Q(title__icontains=keyword) | Q(blog_body__icontains=keyword)
            ),
            "keyword": keyword or "",
        },
    )
