from django import forms
from .models import Country, EntryRegime

class CountryForm(forms.ModelForm):
    class Meta:
        model = Country
        fields = ['full_name', 'short_name', 'code_3', 'code_2']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'short_name': forms.TextInput(attrs={'class': 'form-control'}),
            'code_3': forms.TextInput(attrs={'class': 'form-control'}),
            'code_2': forms.TextInput(attrs={'class': 'form-control'}),
        }

class EntryRegimeForm(forms.ModelForm):
    class Meta:
        model = EntryRegime
        fields = ['regime', 'regulatory_legal_acts', 'note']
        widgets = {
            'regime': forms.TextInput(attrs={'class': 'form-control'}),
            'regulatory_legal_acts': forms.TextInput(attrs={'class': 'form-control'}),
            'note': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }