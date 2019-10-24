from django.urls import path, include, re_path 
from django.contrib.auth import views as auth_views
from django.views.generic import RedirectView
from grocery import views as grocery_views 

urlpatterns = [
   
    path('items/',
        grocery_views.all_grocery,
        name='all_items'),
    
]