from django import forms
from captcha.fields import CaptchaField
from django.core.files import File

from .models import Solution, Exercice

class PostSolutionForm(forms.ModelForm):
    title = forms.CharField(max_length=120, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Solution title'}))
    content = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control', 'placeholder':'Solution description', 'rows':3}))
    file = forms.FileField(widget=forms.FileInput(attrs={'type':'file', 'class':'upload'}))
    captcha = CaptchaField('Are you human?')

    class Meta:
        model = Solution
        fields = ('title', 'content',)

class PostExerciceForm(forms.ModelForm):
    title = forms.CharField(max_length=120)
    content = forms.Textarea()
    file = forms.FileField()
    captcha = CaptchaField('Are you human?')

    class Meta:
        model = Exercice
        fields = ('title', 'content',)
