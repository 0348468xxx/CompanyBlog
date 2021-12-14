from django.db.models import query
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, request
from django.urls import reverse
from django.views.generic import ListView, DetailView
from django.views import View
from .models import Post
from .forms import CommentForm


class StartingPageView(ListView):
    template_name = 'blog/index.html'
    model = Post
    ordering = ['-date']
    context_object_name = 'posts'

    def get_queryset(self):
        queryset = super().get_queryset()
        data = queryset[:3]
        return data


class AllPostView(ListView):
    template_name = 'blog/all-posts.html'
    model = Post
    ordering = ['-date']
    context_object_name = 'all_posts'


class PostDetailView(View):
    def is_marked_post(self, request, post_id):
        marked_posts = request.session.get('marked_posts')
        if marked_posts is not None:
            is_saved_for_later = post_id in marked_posts
        else:
            is_saved_for_later = False

        return is_saved_for_later

    def get(self, request, slug):
        post = Post.objects.get(slug=slug)

        context = {
            "post": post,
            "post_tags": post.tags.all(),
            "comment_form": CommentForm(),
            "comments": post.comments.all().order_by("-id"),
            "saved_for_later": self.is_marked_post(request, post.id)
        }
        return render(request, "blog/post-detail.html", context)

    def post(self, request, slug):
        comment_form = CommentForm(request.POST)
        post = Post.objects.get(slug=slug)

        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.save()

            return HttpResponseRedirect(reverse("post-detail-page", args=[slug]))

        context = {
            "post": post,
            "post_tags": post.tags.all(),
            "comment_form": CommentForm(),
            "comments": post.comments.all().order_by("-id"),
            "saved_for_later": self.is_marked_post(request, post.id)
        }
        return render(request, "blog/post-detail.html", context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post_tags'] = self.object.tags.all()
        context['comment_form'] = CommentForm()
        return context


class ReadLaterView(View):
    def get(self, request):
        marked_posts = request.session.get("marked_posts")
        context = {}

        if marked_posts is None or len(marked_posts) == 0:
            context["posts"] = []
            context["has_posts"] = False
        else:
            context["posts"] = Post.objects.filter(id__in=marked_posts)
            context["has_posts"] = True

        return render(request, "blog/marked-posts.html", context)

    def post(self, request):
        marked_posts = request.session.get("marked_posts")

        if marked_posts is None:
            marked_posts = []

        post_id = int(request.POST["post_id"])

        if post_id not in marked_posts:
            marked_posts.append(post_id)
            request.session["marked_posts"] = marked_posts
        else:
            marked_posts.remove(post_id)

        request.session["marked_posts"] = marked_posts

        return HttpResponseRedirect("/")
