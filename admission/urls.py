from django.urls import path
from .views import Admission_Status, Admission_Form, documents_upload, admin_applications, admin_application_detail,My_Application, download_application_pdf

urlpatterns = [
    path('apply/', Admission_Form, name='admission_form'),
    path('status/<str:application_number>/',Admission_Status,name='application_status'),
    path('documents/', documents_upload, name='documents_upload'),
    path('my-application/<str:application_number>/',My_Application, name='my_application'),
    path('download-pdf/<str:application_number>/',download_application_pdf,name='download_application_pdf'),

    path('admin/applications/', admin_applications, name='admin_applications'),
    path('admin/application/<str:application_number>/',admin_application_detail,name='admin_application_detail'
),
]