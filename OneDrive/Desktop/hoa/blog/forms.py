from django import forms
from django.forms import fields
from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        exclude = ["post"]
        labels = {
            "text": "Your comment"
        }
