from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Post, Comment 

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title','text','note',)

class UserRegistrationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment 
        fields = ('author', 'text',)
