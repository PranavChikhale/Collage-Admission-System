from django.urls import path
from .views import Admission_Status, Admission_Form

urlpatterns = [
    path('apply/', Admission_Form, name='admission_form'),
    path('status/<str:application_number>/',Admission_Status,name='application_status'),
]