from django.shortcuts import get_object_or_404, render

from .models import Blog, Category

def posts_by_category(request, category_id):
    posts = Blog.objects.filter(status='Published', category=category_id)
    category = get_object_or_404(Category, pk=category_id)
    return render(request, 'posts_by_category.html', {
        'posts': posts,
        'category': category,
    } )