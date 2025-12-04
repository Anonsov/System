from django import forms
from django.db import models
from django_ace import AceWidget


class CodeForm(forms.Form):
    class LanguageChoices(models.TextChoices):
        PYTHON = 'python', 'Python'
        CPP = 'cpp', 'C++'
        JAVA = 'java', 'Java'
        JAVASCRIPT = 'javascript', 'JavaScript'

    language = forms.ChoiceField(
        choices=LanguageChoices.choices,
        initial=LanguageChoices.PYTHON,
        widget=forms.Select(attrs={'class': 'language-select'})
    )
    code_area = forms.CharField(
        widget=AceWidget(
            mode='python',
            theme='monokai',
            width="100%",
            height="350px",
            showprintmargin=False,
            fontsize="14px",
            toolbar=True,
            basicautocompletion=True,
            liveautocompletion=True,
        ),
        required=True
    )
    
    # def send_code(self)
