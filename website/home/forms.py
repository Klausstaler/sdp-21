from django import forms

class jsonForm(forms.Form):
    text = forms.CharField(label = 'JSON',max_length=10000000)