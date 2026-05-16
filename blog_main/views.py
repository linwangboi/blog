
from django.shortcuts import render

from blogs.models import Blog, Category


def home(request):
    featured_posts = Blog.objects.filter(is_featured=True).order_by('updated_at')
    posts = Blog.objects.filter(is_featured=False, status='Published')
    
    return render(request, 'home.html', {
        'featured_posts': featured_posts,
        'posts': posts,
    })