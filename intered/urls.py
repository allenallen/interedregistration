"""intered URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import include, static, url
from django.conf import settings
from django.conf.urls.static import static

from registration import views
from registration.views import SchoolNewPopup, get_school_id

urlpatterns = [
    url(r'^admin/', admin.site.urls),
]
urlpatterns += [
    url(r'^s3direct/', include('s3direct.urls')),
]
# urlpatterns += [
#     path('registration/', include('registration.urls'))
# ]
urlpatterns += [
    path('event/<str:uuid>', views.registration, name='register'),
    path('students/extract', views.extractStudents, name='extract'),
    url(r'^register/school/create', SchoolNewPopup, name="schoolNew"),
    url(r'^register/school/ajax/get_school_id', get_school_id, name="get_school_id")
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
