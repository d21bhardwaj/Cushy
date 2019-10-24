from django.contrib import admin
from django.urls import path, include, re_path 
from django.contrib.auth import views as auth_views
from django.views.generic import RedirectView
from grocery import views
#Login
from accounts import views as accounts_views
from django.contrib.auth import logout

urlpatterns = [    
    path('grocery/', 
        views.all_grocery, 
        name='Grocery'),
   
]