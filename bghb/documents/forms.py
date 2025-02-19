from django import forms
from .models import DocumentType, DocumentFeature, FeatureDetail

class FeatureDetailForm(forms.ModelForm):
    class Meta:
        model = FeatureDetail
        fields = ['key', 'value', 'image']


class DocumentFeatureForm(forms.ModelForm):
    class Meta:
        model = DocumentFeature
        fields = ['feature_name']


class DocumentTypeForm(forms.ModelForm):
    class Meta:
        model = DocumentType
        fields = [
            'code', 'name', 'category', 'type', 'first_issue_date', 'valid', 
            'legal_status', 'length', 'width', 'pages', 'validity_period', 
            'renewable', 'issuing_country'
        ]