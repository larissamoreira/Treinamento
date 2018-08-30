from django import forms
from forum import models

class PostForm(forms.ModelForm):

    class Meta:
        model = models.Post
        exclude = []
        widgets = {'usuario': forms.HiddenInput()}

class CommentForm(forms.ModelForm):
    class Meta:
        model = models.Comment
        exclude = []
        widgets = {'usuario': forms.HiddenInput(), 'post': forms.HiddenInput()}