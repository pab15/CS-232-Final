from django import forms
from .models import Profile
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class UserRegisterForm(UserCreationForm):
  class Meta:
    model = User
    fields = ['username', 'email', 'password1', 'password2']
  username = forms.CharField(widget=forms.TextInput(attrs={'class': 'white-text'}))
  email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'white-text'}))
  password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'white-text'}))
  password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'white-text'}))

class UserUpdateForm(forms.ModelForm):
  class Meta:
    model = User
    fields = ['username', 'email']
  email = forms.EmailField()
  bio = forms.Textarea()

class ProfileUpdateForm(forms.ModelForm):
  class Meta:
    model = Profile
    fields = ['bio']


  