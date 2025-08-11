from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RegisterFrom(UserCreationForm):
    email = forms.EmailField(required=True)
    class Mate:
        model = User 
        fields = ['username','email','password1','password2']