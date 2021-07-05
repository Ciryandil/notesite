from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Post, Comment, UserProfile
from django.contrib.auth.models import User
class PostForm(forms.ModelForm):

    
    class Meta:
        model = Post
        fields = ('title','text','note','tags',)

class UserRegistrationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = User

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment 
        fields = ('text',)

class UserProfileForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = ('dp',)
        

