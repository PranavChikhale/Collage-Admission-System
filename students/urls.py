from django.urls import path
from .views import Profile_View,view_applications

urlpatterns = [
    path('profile/', Profile_View, name='student_profile'),
    path('applications/',view_applications,name='view_applications'),
]