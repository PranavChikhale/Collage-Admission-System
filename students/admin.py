from django.contrib import admin
from .models import StudentProfile

@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):

    list_display = ('user', 'mobile', 'gender', 'category', 'city', 'state',)
    search_fields = ('user_name', 'user_email', ' mobile',)
    list_filter = ('gender', 'category', 'state',)
