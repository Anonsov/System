from django import forms
from django_ace import AceWidget


class CodeForm(forms.Form):
    LANGUAGE_CHOICES = [
        ('python', 'Python'),
        ('cpp', 'C++'),
        ('java', 'Java'),
        ('javascript', 'JavaScript'),
     
    ]
        
    language = forms.ChoiceField(
    choices=LANGUAGE_CHOICES,
    initial='python',
    widget=forms.Select(attrs={'class': 'language-select'})
    )
    code_area = forms.CharField(
        widget=AceWidget(
            mode='python',
            theme='twilight',
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
