from django.contrib import admin
from django.urls import path, include, re_path 
from django.contrib.auth import views as auth_views
from django.views.generic import RedirectView
from main import views
#Login

from django.contrib.auth import logout
from django.conf import settings
urlpatterns = [

    path('', views.index, name='index'),
    path('', include('social_django.urls', namespace='social')),
    path('logout/', views.logout_view, name='logout'),
]