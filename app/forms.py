from django import forms
from .models import Post,Comment,Profile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('image','name', 'caption')

class SignUpForm(UserCreationForm):
   

    class Meta:
        model = User
        fields = ('username',  'password1', 'password2', )

class CommentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['comment'].widget = forms.TextInput()
        self.fields['comment'].widget.attrs['placeholder'] = 'Add a comment...'
    class Meta:
        model = Comment
        fields = ('comment',)

class UpdateUserProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile', 'bio']

