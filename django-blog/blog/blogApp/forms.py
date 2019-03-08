from django import forms
from .models import Comment, Post
from pagedown.widgets import PagedownWidget

class Update_Post(forms.ModelForm):
    content = forms.CharField(widget=PagedownWidget(attrs = {'class':'form-control',}))

    title = forms.CharField(widget=forms.TextInput(
            attrs = {'class':'form-control','placeholder':'Post title'}
    ))

    class Meta:
        model = Post
        fields = [
            'title',
            'category',
            'author',
            'content',
            'image',
            'status',
        ]



class CommentForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(
            attrs = {'class':'form-control','placeholder':'Enter your name'}
    ))

    comments = forms.CharField(widget=forms.TextInput(
            attrs = {'class':'form-control form-control-lg','placeholder':'Enter comment'}
    ))

    class Meta:
        model = Comment
        fields = [
            'name','comments'
        ]
