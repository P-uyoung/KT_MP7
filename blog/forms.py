# blog/forms.py
from django import forms
from . import models

class PostModelForm(forms.ModelForm):
    class Meta:
        model = models.Post
        fields = ('title', 'content', 'published_at')

class PostForm(forms.Form):
    title = forms.CharField(max_length=100)
    content = forms.CharField(widget=forms.Textarea())
    published = forms.DateField()
