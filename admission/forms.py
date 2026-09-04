from django import forms
from .models import AdmissionApplication, AcademicDetails
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
            'tenth_percentage', 'tenth_board', 'tenth_collage', 'tenth_passing_year',
            'twelfth_percentage', 'twelfth_board', 'twelfth_collage',
        ]