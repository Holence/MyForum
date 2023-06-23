from django import forms
from .models import Comment
from martor.fields import MartorFormField

class CommentForm(forms.ModelForm):
    content = MartorFormField()
    class Meta:
        model = Comment
        fields = ["content"]
