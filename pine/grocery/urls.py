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
    path('upload/',
        views.data_upload,
        name='Upload_data'),
    path('cart/',
        views.cart_add,
        name='Cart_add'),
    path('shops/',
        views.all_shops,
        name='All_Shops'),

#--- Add whatever you want above it --#
    ## Always keep it Last in path ###
    path('<str:shop_name>/',
        views.shops_grocery,
        name='Shops_Grocery'),
    #--- Don't add any thing below this -- #
]