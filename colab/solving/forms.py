from django import forms
from captcha.fields import CaptchaField

from .models import Solution

class PostSolutionForm(forms.ModelForm):
    title = forms.CharField(max_length=120)
    content = forms.Textarea()
    captcha = CaptchaField('Are you human?')

    class Meta:
        model = Solution
        fields = ('title', 'content',)
