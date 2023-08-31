from django                     import forms
from django.contrib.auth.forms  import UserCreationForm
from django.contrib.auth.models import User

from .models import *

class RegistroForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=50, required=True)
    last_name = forms.CharField(max_length=50, required=True)
    
    class Meta:
        model = User
        fields = ['first_name','last_name','username', 'email', 'password1', 'password2']

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'category']


class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']


