"""pine URL Configuration

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
from django.urls import path, include, re_path 
from django.contrib.auth import views as auth_views
from django.views.generic import RedirectView
from main import views
#Login
from django.contrib.auth import logout
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('dashtown/', admin.site.urls),
    path('',include('main.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/profile/', RedirectView.as_view(pattern_name='index', permanent=False)),
    
    path('', views.index, name='index'),
    path('',include('accounts.urls')),
    path('grocery/',include('grocery.urls')),
    
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
