# from django import forms
# from .models import CertificateTemplate

# class CertificateTemplateForm(forms.ModelForm):
#     class Meta:
#         model = CertificateTemplate
#         fields = ['name', 'file']

# class TemplateForm(forms.ModelForm):
#     class Meta:
#         model = CertificateTemplate
#         fields = ['name', 'file']

from django import forms
from .models import CertificateTemplate

class CertificateTemplateForm(forms.ModelForm):
    class Meta:
        model = CertificateTemplate
        fields = ['name', 'certificate_type', 'file']  # include new field

class TemplateForm(forms.ModelForm):
    class Meta:
        model = CertificateTemplate
        fields = ['name', 'file']