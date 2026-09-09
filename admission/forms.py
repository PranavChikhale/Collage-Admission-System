from django import forms
from .models import AdmissionApplication, AcademicDetails, StudentDocuments
from course.models import Course


class AdmissionApplicationForm(forms.ModelForm):
    class Meta:
        model = AdmissionApplication
        fields = [
            'course',
        ]
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['course'].queryset = Course.objects.filter(is_active=True, available_seats__gt = 0)

class AcademicDetailsForm(forms.ModelForm):

    class Meta:
        model = AcademicDetails

        fields = [
            'tenth_percentage',
            'tenth_collage',
            'tenth_board',
            'tenth_passing_year',

            'twelfth_percentage',
            'twelfth_collage',
            'twelfth_board',
            'twelfth_passing_year',
        ]

        labels = {
            'tenth_percentage': '10th Percentage',
            'tenth_collage': '10th School / College',
            'tenth_board': '10th Board',
            'tenth_passing_year': '10th Passing Year',

            'twelfth_percentage': '12th Percentage',
            'twelfth_collage': '12th School / College',
            'twelfth_board': '12th Board',
            'twelfth_passing_year': '12th Passing Year',
        }

        widgets = {

            'tenth_percentage': forms.NumberInput(
                attrs={
                    'placeholder': 'Enter 10th percentage',
                    'step': '0.01',
                    'min': '0',
                    'max': '100'
                }
            ),

            'tenth_collage': forms.TextInput(
                attrs={
                    'placeholder': 'Enter school / college name'
                }
            ),

            'tenth_board': forms.TextInput(
                attrs={
                    'placeholder': 'e.g. Maharashtra State Board'
                }
            ),

            'tenth_passing_year': forms.NumberInput(
                attrs={
                    'placeholder': 'e.g. 2024'
                }
            ),

            'twelfth_percentage': forms.NumberInput(
                attrs={
                    'placeholder': 'Enter 12th percentage',
                    'step': '0.01',
                    'min': '0',
                    'max': '100'
                }
            ),

            'twelfth_collage': forms.TextInput(
                attrs={
                    'placeholder': 'Enter school / college name'
                }
            ),

            'twelfth_board': forms.TextInput(
                attrs={
                    'placeholder': 'e.g. Maharashtra State Board'
                }
            ),

            'twelfth_passing_year': forms.NumberInput(
                attrs={
                    'placeholder': 'e.g. 2026'
                }
            ),
        }

class StudentDocumentsForm(forms.ModelForm):

    class Meta:
        model = StudentDocuments

        fields = [
            'photo',
            'signature',
            'tenth_marksheet',
            'twelfth_marksheet',
            'leaving_certificate',
            'caste_certificate',
        ]

        labels = {
            'photo': 'Passport Size Photo',
            'signature': 'Signature',
            'tenth_marksheet': '10th Marksheet',
            'twelfth_marksheet': '12th Marksheet',
            'leaving_certificate': 'Leaving Certificate',
            'caste_certificate': 'Caste Certificate',
        }

        widgets = {
            'photo': forms.FileInput(
                attrs={
                    'accept': 'image/*'
                }
            ),

            'signature': forms.FileInput(
                attrs={
                    'accept': 'image/*'
                }
            ),

            'tenth_marksheet': forms.FileInput(
                attrs={
                    'accept': '.pdf,.jpg,.jpeg,.png'
                }
            ),

            'twelfth_marksheet': forms.FileInput(
                attrs={
                    'accept': '.pdf,.jpg,.jpeg,.png'
                }
            ),

            'leaving_certificate': forms.FileInput(
                attrs={
                    'accept': '.pdf,.jpg,.jpeg,.png'
                }
            ),

            'caste_certificate': forms.FileInput(
                attrs={
                    'accept': '.pdf,.jpg,.jpeg,.png'
                }
            ),
        }