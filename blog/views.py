from django.db.models import query
from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponseRedirect, request
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, DeleteView
from django.views import View
from django.db.models import Q
from .models import Comment, Post
from .forms import CommentForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin

# login require
from django.utils.decorators import method_decorator

def class_view_decorator(function_decorator):
    """Convert a function based decorator into a class based decorator usable
    on class based Views.

    Can't subclass the `View` as it breaks inheritance (super in particular),
    so we monkey-patch instead.
    """

    def simple_decorator(View):
        View.dispatch = method_decorator(function_decorator)(View.dispatch)
        return View

    return simple_decorator

# Impleting functions for Homepage 
@class_view_decorator(login_required)
class StartingPageView(ListView):
    template_name = 'blog/index.html'
    model = Post
    ordering = ['-date']
    context_object_name = 'posts'  # Designates the name of the variable to use in the context.

    #Get the list of items for this view.In this case: 3 posts
    def get_queryset(self): 
        queryset = super().get_queryset()
        data = queryset[:3]
        return data

# Impleting functions for All Posts Page
@class_view_decorator(login_required)
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
@class_view_decorator(login_required)
class PostDetailView(View, LoginRequiredMixin):
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
            comment.author = request.user
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

@class_view_decorator(login_required)
class CommentReplyView(View):
    def post(self, request, slug, pk):
        post = Post.objects.get(slug=slug)
        parent_comment = Comment.objects.get(pk=pk)
        form = CommentForm(request.POST)

        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.post = post
            new_comment.parent = parent_comment
            new_comment.author = request.user
            new_comment.save()
    
        return redirect('post-detail-page', slug=slug)
        



# Impleting functions for Marked Posts Page
@class_view_decorator(login_required)
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


@class_view_decorator(login_required)
class DeleteComment(DeleteView):
    model = Comment
    template_name = "blog/delete-comment.html"
    def get_success_url(self):
         return reverse('post-detail-page', args=(self.kwargs['slug'],))
        

    