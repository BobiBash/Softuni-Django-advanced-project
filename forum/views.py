from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DetailView

from forum.models import ForumPost


# Create your views here.
class ForumPostsListView(LoginRequiredMixin, ListView):
    model = ForumPost
    template_name = 'forum/forum-posts-list.html'

class ForumCreatePostView(LoginRequiredMixin, CreateView):
    model = ForumPost
    template_name = 'forum/forum-create-post.html'
    fields = ('title', 'content')


class ForumUpdatePostView(LoginRequiredMixin, UpdateView):
    model = ForumPost
    template_name = 'forum/forum-edit-post.html'
    fields = 'title', 'content'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post'] = self.get_object()
        return context

class ForumPostDetailView(LoginRequiredMixin, DetailView):
    model = ForumPost
    template_name = 'forum/forum-view-post.html'