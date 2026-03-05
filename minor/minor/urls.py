"""
URL configuration for minor project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path, re_path
from django.http import HttpResponse
from myapp import views

# Handler for Chrome DevTools requests
def chrome_devtools_handler(request):
    return HttpResponse(status=204)  # No Content response

urlpatterns = [
    path('', views.home, name='home'),
    path('appointment', views.appointment, name='appointment'),
    path('disease_info', views.disease_info, name='disease_info'),
    path('page1', views.page1, name='page1'),
    path('page2', views.page2, name='page2'),
    path('page3', views.page3, name='page3'),
    path('page4', views.page4, name='page4'),
    path('page5', views.page5, name='page5'),
    path('page6', views.page6, name='page6'),
    path('page7', views.page7, name='page7'),
    path('page8', views.page8, name='page8'),
    path('page9', views.page9, name='page9'),
    path('page10', views.page10, name='page10'),
    path('register', views.register, name='register'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('predict', views.predict, name='predict'),
    path('camera-capture', views.camera_capture, name='camera_capture'),
    path('predict-api', views.predict_api, name='predict_api'),
    path('result', views.result, name='result'),
    path('check-auth', views.check_auth_status, name='check_auth'),
    path('admin/', admin.site.urls),
    # Handle Chrome DevTools requests silently
    re_path(r'^\.well-known/.*', chrome_devtools_handler),
]
