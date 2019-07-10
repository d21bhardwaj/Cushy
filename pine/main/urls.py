from django.contrib import admin
from django.urls import path, include, re_path 
from django.contrib.auth import views as auth_views
from django.views.generic import RedirectView
from main import views
#Login
from accounts import views as accounts_views
from django.contrib.auth import logout

#Account view



#########################################

urlpatterns = [
    
    path('', include('social_django.urls', namespace='social')),
    path('logout/', views.logout_view, name='logout'),
    path('Rentform/', views.rentdetails, name='RentForm'),
    path('ChooseType/', views.renttype, name='RentType'),
    path('RentPGForm/', views.rentpgdetails, name='RentPGForm'),
    #Rooms and Pgs
    path('Rooms/', views.allrooms, name='all_rooms'),
    path('Pgs/', views.allpgs, name='all_pgs'),
    path('<int:room_id>/RoomDetails/<int:image_id>/', views.detailroom, name='room_detail'),
    path('<int:room_id>/PGDetails/<int:image_id>/', views.detailpg, name='pg_detail'),
#Adding url password related form the link(https://simpleisbetterthancomplex.com/series/2017/09/25/a-complete-beginners-guide-to-django-part-4.html)

    path('Privacy-Policy/', views.privacy, name='privacy-policy'),
#Contact Us View
    path('contact_us/', 
        views.contact, 
        name='contact_us'),
]