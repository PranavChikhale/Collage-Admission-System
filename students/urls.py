from django.urls import path
from .views import Profile_View

urlpatterns = [
    path('profile/', Profile_View, name='student_profile'),
]