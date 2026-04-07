from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView

from forum.forms import ForumCommentForm, ForumCreatePostForm, TagForm
from forum.models import ForumPost, Comment, Tag


# Create your views here.
class ForumPostsListView(LoginRequiredMixin, ListView):
    model = ForumPost
    template_name = 'forum/forum-posts-list.html'

class ForumCreatePostView(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    model = ForumPost
    form_class = ForumCreatePostForm
    template_name = 'forum/forum-create-post.html'
    permission_required = 'forum.add_forumpost'
    success_url = reverse_lazy('forum-posts-list')

    def form_valid(self, form):
        form.instance.author_id = self.request.user.id
        return super().form_valid(form)


class ForumUpdatePostView(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    model = ForumPost
    template_name = 'forum/forum-edit-post.html'
    form_class = ForumCreatePostForm
    permission_required = 'forum.change_forumpost'
    success_url = reverse_lazy('forum-posts-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post'] = self.get_object()
        return context

    def get_queryset(self):
        return ForumPost.objects.filter(author_id=self.request.user.id)

class ForumPostDetailView(LoginRequiredMixin, View):
    def get(self, request, pk):
        post = get_object_or_404(ForumPost, pk=pk)
        form = ForumCommentForm()
        comments = Comment.objects.filter(post_id=pk)

        context = {
            'post': post,
            'comments': comments,
            'form': form
        }

        return render(request, 'forum/forum-view-post.html', context)


class ForumPostDeleteView(PermissionRequiredMixin, LoginRequiredMixin, DeleteView):
    model = ForumPost
    template_name = 'forum/forum-delete-post.html'
    permission_required = 'forum.delete_forumpost'
    success_url = reverse_lazy('forum-posts-list')

    def get_queryset(self):
        return ForumPost.objects.filter(author_id=self.request.user.id)


class ForumCreateCommentView(PermissionRequiredMixin, LoginRequiredMixin, View):
    permission_required = 'forum.add_comment'

    def post(self, request, pk):
        form = ForumCommentForm(request.POST)
        print(form.errors)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post_id = pk
            comment.save()
            return redirect('forum-post-details', pk=pk)

        post = get_object_or_404(ForumPost, pk=pk)
        comments = Comment.objects.filter(post_id=pk)
        return render(request, 'forum/forum-view-post.html', {
            'post': post,
            'form': form,
            'comments': comments,
        })

class ForumUpdateCommentView(PermissionRequiredMixin, LoginRequiredMixin, View):
    permission_required = 'forum.change_comment'

    def post(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk, author_id=request.user.id)
        comment.content = request.POST.get('content')
        comment.save()
        return redirect('forum-post-details', pk=comment.post_id)

class ForumDeleteCommentView(PermissionRequiredMixin, LoginRequiredMixin, View):
    permission_required = 'forum.delete_comment'

    def post(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk, author_id=request.user.id)
        comment.delete()
        return redirect("forum-post-details", pk=comment.post_id)


class TagListView(LoginRequiredMixin, ListView):
    model = Tag
    template_name = "forum/tag_list.html"
    context_object_name = "tags"


class TagCreateView(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    model = Tag
    form_class = TagForm
    template_name = "forum/tag_create.html"
    permission_required = "forum.add_tag"
    success_url = reverse_lazy("tag-list")


class TagUpdateView(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    model = Tag
    form_class = TagForm
    template_name = "forum/tag_update.html"
    permission_required = "forum.change_tag"
    success_url = reverse_lazy("tag-list")


class TagDeleteView(PermissionRequiredMixin, LoginRequiredMixin, DeleteView):
    model = Tag
    template_name = "forum/tag_delete.html"
    permission_required = "forum.delete_tag"
    success_url = reverse_lazy("tag-list")


class TagDetailView(LoginRequiredMixin, DetailView):
    model = Tag
    template_name = "forum/tag_detail.html"
    context_object_name = "tag"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["posts"] = self.object.posts.all()
        return context
