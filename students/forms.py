from django import forms
from .models import  StudentProfile

class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = StudentProfile

        fields = ['mobile', 'date_of_birth', 'gender','category','address','city','state','pincode']

        widgets = {
            'date_of_birth': forms.DateInput( attrs={'type': 'date'}),
            'address': forms.Textarea( attrs={'rows': 4}),
        }


