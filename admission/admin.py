from django.contrib import admin
from .models import AdmissionApplication, AcademicDetails


@admin.register(AdmissionApplication)
class AdmissionApplicationAdmin(admin.ModelAdmin):
    list_display = (
        'application_number','student','course','application_date','status'
    )
    list_filter = (
        'status', 'course'
    )
    search_fields = (
        'application_number', 'student_email','student_username'
    )

@admin.register(AcademicDetails)
class AcademicDetailsAdmin(admin.ModelAdmin):

    list_display = (
        'application',
        'tenth_percentage','tenth_board','tenth_collage', 'tenth_passing_year',
        'twelfth_percentage','twelfth_board','twelfth_collage',
    )

    search_fields = (
        'application__application_number', 'application__student_username',
    )