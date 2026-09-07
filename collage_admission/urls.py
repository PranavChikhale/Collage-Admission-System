from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('django-admin/', admin.site.urls),
    path('', include('account.urls')),
    path('student/',include('students.urls')),
    path('course/',include('course.urls')),
    path('admission/',include('admission.urls')),
    path('captcha/', include('captcha.urls')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)