# from django import forms
# from .models import Candidate

# class CandidateForm(forms.ModelForm):
#     class Meta:
#         model = Candidate
#         fields = '__all__'
#         exclude = ['company']

# class UploadFileForm(forms.Form):
#     file = forms.FileField(label='Select an Excel file (.xlsx)')

#     def clean_file(self):
#         file = self.cleaned_data.get('file')
#         if not file.name.endswith('.xlsx'):
#             raise forms.ValidationError("Only .xlsx files are supported.")
#         return file


from django import forms
from .models import Candidate

class CandidateForm(forms.ModelForm):
    class Meta:
        model = Candidate
        fields = '__all__'
        exclude = ['company']
        widgets = {
            'project_title': forms.TextInput(attrs={
                'class': 'form-control',  # or any additional class for styling
                'placeholder': 'Enter project details',
                'style': 'height: 40px;'  # makes it smaller
            }),
            # Optional: you can customize other fields similarly
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'usn': forms.TextInput(attrs={'class': 'form-control'}),
            'department': forms.TextInput(attrs={'class': 'form-control'}),
            'college': forms.TextInput(attrs={'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
        }


class UploadFileForm(forms.Form):
    file = forms.FileField(label='Select an Excel file (.xlsx)')

    def clean_file(self):
        file = self.cleaned_data.get('file')
        if not file.name.endswith('.xlsx'):
            raise forms.ValidationError("Only .xlsx files are supported.")
        return file
