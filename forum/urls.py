from django.urls import path

from forum.views import ForumPostsListView, ForumCreatePostView, ForumUpdatePostView, ForumPostDetailView

urlpatterns = [
    path('', ForumPostsListView.as_view(), name='forum-posts-list'),
    path('create-post', ForumCreatePostView.as_view(), name='forum-post-create'),
    path('edit-post/<int:pk>', ForumUpdatePostView.as_view(), name='forum-edit-post'),
    path('post-details/<int:pk>', ForumPostDetailView.as_view(), name='forum-post-details')

]