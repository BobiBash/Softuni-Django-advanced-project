from django import forms

from forum.models import ForumPost, Comment


class ForumPostsForm(forms.ModelForm):

    class Meta:
        model = ForumPost
        fields = "__all__"

class ForumCreatePostForm(forms.ModelForm):

    class Meta:
        model = ForumPost
        fields = ('title', 'content')

        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'p-2 border rounded-sm w-md focus:outline-none'
            }),
            'content': forms.Textarea(attrs={
                'class': 'p-1 border rounded-sm w-md focus:outline-none',
                'style': 'resize:none'
            })
        }


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