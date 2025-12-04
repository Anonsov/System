from django import forms 
from django_ace import AceWidget

class ReadOnlyCodeForm(forms.Form):
    code_area = forms.CharField(
        widget=AceWidget(
            mode='python',
            theme='twilight',
            width="100%",
            height="350px",
            showprintmargin=False,
            fontsize="14px",
            toolbar=False,
            readonly=True,
        ),
        required=False
    )