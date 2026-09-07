from django.urls import path
from .views import Admission_Status, Admission_Form, documents_upload, admin_applications, admin_application_detail

urlpatterns = [
    path('apply/', Admission_Form, name='admission_form'),
    path('status/<str:application_number>/',Admission_Status,name='application_status'),
    path('documents/', documents_upload, name='documents_upload'),
    path('admin/applications/', admin_applications, name='admin_applications'),
    path('admin/application/<str:application_number>/',admin_application_detail,name='admin_application_detail'
),
]