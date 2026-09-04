from django.urls import path
from .views import CourseList

urlpatterns = [
    path('',CourseList,name='course_list'),
]