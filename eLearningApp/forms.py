# Import necessary modules
from django import forms
from .models import *
from django.contrib.auth.models import User

class UserForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['email', 'password1', 'password2', 'first_name', 'last_name']
        
class AppUserForm(forms.ModelForm):
    class Meta:
        model = AppUser
        fields = ['institution']