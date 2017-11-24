from django import forms
from captcha.fields import CaptchaField
from django.core.files import File
from django.contrib.auth.forms import AuthenticationForm
from django.forms.widgets import PasswordInput, TextInput

from .models import Solution, Exercice

class PostSolutionForm(forms.ModelForm):
    title = forms.CharField(max_length=120, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Solution title'}))
    content = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control', 'placeholder':'Solution description', 'rows':3}))
    file = forms.FileField(widget=forms.FileInput(attrs={'type':'file', 'class':'upload'}))
    captcha = CaptchaField('Are you human?')

    class Meta:
        model = Solution
        fields = ('title', 'content',)

class EditSolutionForm(forms.ModelForm):
    title = forms.CharField(max_length=120, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Solution title'}))
    content = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control', 'placeholder':'Solution description', 'rows':3}))
    captcha = CaptchaField('Are you human?')

    class Meta:
        model = Solution
        fields = ('title', 'content',)

class PostExerciceForm(forms.ModelForm):
    title = forms.CharField(max_length=120, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Exercice title'}))
    content = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control', 'placeholder':'Solution description', 'rows':3}))
    file = forms.FileField(widget=forms.FileInput(attrs={'type':'file', 'class':'upload'}))
    captcha = CaptchaField('Are you human?')

    class Meta:
        model = Exercice
        fields = ('title', 'content',)

class EditExerciceForm(forms.ModelForm):
    title = forms.CharField(max_length=120, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Exercice title'}))
    content = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control', 'placeholder':'Solution description', 'rows':3}))
    captcha = CaptchaField('Are you human?')

    class Meta:
        model = Exercice
        fields = ('title', 'content',)
