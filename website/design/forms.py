from django import forms
from .models import package

class packageCreateForm(forms.ModelForm):

    class Meta:
        model = package
        fields =[
            'id',
            'shelf',
            'shelf_compartment',
            'weight',
            'length',
            'width',
            'height',
            'details',
        ]
class packagePickForm(forms.Form):
    class Meta:
        model = package
    package = forms.ModelMultipleChoiceField(queryset = package.objects.all(),widget=forms.CheckboxSelectMultiple,label='')

