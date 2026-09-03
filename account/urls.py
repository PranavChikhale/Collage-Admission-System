from django.urls import path
from .views import (login_view,register_view,logout_view,STUDENT_DASHBOARD,ADMIN_DASHBORAD,HOME)


urlpatterns = [
    path('',HOME,name='home'),
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logout'),

    path('student/dashboard/',STUDENT_DASHBOARD,name='student_dashboard'),
    path('admin/dashboard/',ADMIN_DASHBORAD,name='admin_dashboard'),
]