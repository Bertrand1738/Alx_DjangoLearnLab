from django.shortcuts import render
from .models import Post

# Create your views here.

def post_list(request):
    """Display all blog posts"""
    posts = Post.objects.all()
    return render(request, 'blog/post_list.html', {'posts': posts})
