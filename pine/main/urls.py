from django.contrib import admin
from django.urls import path, include, re_path 
from django.contrib.auth import views as auth_views
from django.views.generic import RedirectView
from main import views

urlpatterns = [
    path('', views.index, name='index'),
]