from django import forms

from forum.models import ForumPost, Comment


class ForumPostsForm(forms.ModelForm):

    class Meta:
        model = ForumPost
        fields = "__all__"


class ForumCommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('content',)


        widgets = {
            'content': forms.Textarea(attrs={
                'rows': 3,
                'cols': 40,
                'style': 'resize:none',
                'class': 'border p-2 m-2 rounded-sm focus:outline-none',
                'placeholder': 'Add a comment...'
            })
        }

        error_messages = {
            'content': {
                'required': 'This field is required',
            }
        }