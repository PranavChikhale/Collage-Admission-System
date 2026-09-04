from django.shortcuts import render, redirect
from .models import Course

def CourseList(request):
    courses = Course.objects.filter(is_active=True)

    return render(request, 'course/course_list.html', {'courses': courses})