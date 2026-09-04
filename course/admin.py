from django.contrib import admin
from .models import Course

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('course_name', 'course_code',
                    'department','duration',
                    'total_seats','available_seats',
                    'is_active')

    search_fields = ('course_name', 'course_code', 'department')

    list_filter = ('department', 'is_active')