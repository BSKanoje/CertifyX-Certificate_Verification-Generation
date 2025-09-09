from django import forms
from .models import Company

class CompanyProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['company_name', 'phone', 'logo', 'address'] # Exclude email as it's the USERNAME_FIELD
        widgets = {
            'address': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Bootstrap classes to fields
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            # Add placeholders for better UX
            if field_name == 'company_name':
                field.widget.attrs['placeholder'] = 'Your Company Name'
            elif field_name == 'phone':
                field.widget.attrs['placeholder'] = 'e.g., +1234567890'
            elif field_name == 'address':
                field.widget.attrs['placeholder'] = 'Your Company Address'