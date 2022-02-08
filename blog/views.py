from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from blog.models import Post, Tag
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from blog.tasks import random_tag_post


class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-created_at', '-updated_at']
    paginate_by = 3
    queryset = Post.objects.prefetch_related('author')


class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_post.html'
    context_object_name = 'posts'
    paginate_by = 2

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-created_at')


class PostDetailView(DetailView):
    model = Post


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        response = super(PostCreateView, self).form_valid(form)

        random_tag_post.delay(self.object.id)

        return response


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author


def about(request):
    return render(request, 'blog/about.html')


class TagListView(ListView):
    model = Tag
    template_name = 'blog/tags.html'
    context_object_name = 'tags'


class TagPostListView(ListView):
    model = Post
    template_name = 'blog/tag_post.html'
    context_object_name = 'posts'
    paginate_by = 3

    def get_queryset(self):
        tag = get_object_or_404(Tag, pk=self.kwargs.get('pk'))
        self.tag_for_context = tag # TODO: Check other solutions :|
        return Post.objects.filter(tag__in=[tag.id]).order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = {'tag': self.tag_for_context}
        kwargs.update(context)
        return super().get_context_data(**kwargs)
