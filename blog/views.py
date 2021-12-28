from django.db.models import query
from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponseRedirect, request
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, DeleteView
from django.views import View
from django.db.models import Q
from .models import Comment, Post
from .forms import CommentForm

# Impleting functions for Homepage 
class StartingPageView(ListView):
    template_name = 'blog/index.html'
    model = Post
    ordering = ['-date']
    context_object_name = 'posts'

    def get_queryset(self):
        queryset = super().get_queryset()
        data = queryset[:3]
        return data

# Impleting functions for All Posts Page
class AllPostView(ListView):
    template_name = 'blog/all-posts.html'
    model = Post
    ordering = ['-date']
    context_object_name = 'all_posts'
    # queryset = Post.objects.filter(title__icontains='IFI') # Basic Filtering

    def get_queryset(self):
        search_query = self.request.GET.get('search_query')
        object_list = self.model.objects.all()
        if search_query: 
            object_list = object_list.filter(
                Q(title__icontains=search_query) | Q(content__icontains=search_query) | Q(excerpt__icontains=search_query))
        return object_list

        # return Post.objects.filter(title__icontains='IFI')


# Impleting functions for Single Post Page
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
        # parent_obj = None

        # try:
        #     parent_id = request.POST.get("parent_id")
        # except:
        #     parent_id = None

        # if parent_id:
        #     parent_qs = Comment.objects.filter( id=parent_id)
        #     if parent_qs.exists() and parent_qs.count() == 1:
        #         parent_obj = parent_qs.first()

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
            # "parent": parent_obj
        }
        return render(request, "blog/post-detail.html", context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post_tags'] = self.object.tags.all()
        context['comment_form'] = CommentForm()
        return context

class CommentReplyView(View):
    def post(self, request, slug, pk):
        post = Post.objects.get(slug=slug)
        parent_comment = Comment.objects.get(pk=pk)
        form = CommentForm(request.POST)

        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.post = post
            new_comment.parent = parent_comment
            new_comment.save()
    
        return redirect('post-detail-page', slug=slug)
        



# Impleting functions for Marked Posts Page
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




class DeleteComment(DeleteView):
    model = Comment
    template_name = "blog/delete-comment.html"
    def get_success_url(self):
         return reverse('post-detail-page', args=(self.kwargs['slug'],))
        

    