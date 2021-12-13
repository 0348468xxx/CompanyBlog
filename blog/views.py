from django.shortcuts import render, get_object_or_404
from .models import Post


def starting_page(request):
    last_posts = Post.objects.all().order_by("-date")[:3] # Get 3 current post 
    # last_posts = sorted_posts[-3:]
    return render(request, 'blog/index.html', {
        "posts": last_posts
    })


def posts(request):
    all_posts = Post.objects.all().order_by("-date")
    return render(request, 'blog/all-posts.html', {
        "all_posts": all_posts
    })


def post_detail(request, slug):  # Use slug for dynamic URL
    defined_post = get_object_or_404(Post, slug=slug)
    return render(request, 'blog/post-detail.html', {
        "post": defined_post,
        "post_tags": defined_post.tags.all()
    })
