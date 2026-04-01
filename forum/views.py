from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from forum.models import ForumPost, Comment


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

    def get_queryset(self):
        return ForumPost.objects.filter(author_id=self.request.user.id)

class ForumPostDetailView(LoginRequiredMixin, View):
    def get(self, request, pk):
        post = ForumPost.objects.get(pk=pk)
        comments = Comment.objects.filter(post_id=pk)

        context = {
            'post': post,
            'comments': comments,
        }

        return render(request, 'forum/forum-view-post.html', context)


class ForumPostDeleteView(LoginRequiredMixin, DeleteView):
    model = ForumPost
    template_name = 'forum/forum-delete-post.html'

    def get_queryset(self):
        return ForumPost.objects.filter(author_id=self.request.user.id)


class ForumCreateCommentView(LoginRequiredMixin, View):

    def post(self, request, pk):
        content = request.POST.get('content')

        Comment.objects.create(
            author_id=request.user.id,
            content=content,
            post_id=pk,
        )

        return redirect('forum-post-details', pk=pk)

