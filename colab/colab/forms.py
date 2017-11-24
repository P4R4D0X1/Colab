from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.forms.widgets import PasswordInput, TextInput

class MyAuthenticationForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Username'}))
    password = forms.CharField(widget=PasswordInput(attrs={'class':'form-control', 'placeholder':'Password'}))

class SignupForm(UserCreationForm):
    username = forms.CharField(max_length=120, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Username'}))
    email = forms.EmailField(max_length=120, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Email'}))
    password1 = forms.CharField(widget=PasswordInput(attrs={'class':'form-control', 'placeholder':'Password'}))
    password2 = forms.CharField(widget=PasswordInput(attrs={'class':'form-control', 'placeholder':'Password'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
