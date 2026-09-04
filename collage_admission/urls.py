from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('django-admin/', admin.site.urls),
    path('', include('account.urls')),
    path('student/',include('students.urls')),
    path('course/',include('course.urls')),
    path('admission/',include('admission.urls')),
]