from django import forms

from forum.models import ForumPost, Comment, Tag


class ForumPostsForm(forms.ModelForm):
    class Meta:
        model = ForumPost
        fields = "__all__"


class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ("name",)

        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "p-2 border rounded-sm w-md focus:outline-none",
                }
            ),
        }

        error_messages = {
            "name": {
                "required": "Tag name is required.",
                "unique": "This tag already exists.",
            },
        }


class ForumCreatePostForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        is_editing = self.instance and self.instance.pk
        if is_editing:
            self.fields["title"].widget.attrs.update(
                {
                    "class": "p-2 border rounded-sm w-md focus:outline-none bg-gray-200 cursor-not-allowed",
                    "readonly": "readonly",
                    "disabled": "disabled",
                }
            )
            self.fields["title"].required = False

    def clean_title(self):
        title = self.cleaned_data.get("title")
        if not title and self.instance and self.instance.pk:
            return self.instance.title
        return title

    class Meta:
        model = ForumPost
        fields = ('title', 'content', 'tags')

        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'p-2 border rounded-sm w-md focus:outline-none'
            }),
            'content': forms.Textarea(attrs={
                'class': 'p-1 border rounded-sm w-md focus:outline-none',
                'style': 'resize:none'
            }),
            "tags": forms.CheckboxSelectMultiple,
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