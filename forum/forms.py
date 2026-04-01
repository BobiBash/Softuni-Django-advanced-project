from django import forms

from forum.models import ForumPost, Comment


class ForumPostsForm(forms.ModelForm):

    class Meta:
        model = ForumPost
        fields = "__all__"


class ForumCommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = "__all__"