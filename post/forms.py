from django import forms
from .models import Post, Comment


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ("body",)


class EditPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ("body",)


class AddCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("body",)
        widgets = {
            'body': forms.Textarea(attrs={"class": "form-control"})
        }
        labels = {
            "body": "Comment",
        }


class AddReplyForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("body",)
        widgets = {
            'body': forms.Textarea(attrs={"class": "form-control"})
        }
        labels = {
            "body": "Reply",
        }
