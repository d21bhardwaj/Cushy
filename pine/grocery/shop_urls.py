from django.contrib import admin
from django.urls import path, include, re_path 
from django.contrib.auth import views as auth_views
from django.views.generic import RedirectView
from grocery import views 
#Login
from accounts import views as accounts_views
from django.contrib.auth import logout

urlpatterns = [
    path('cart/',
        views.cart_add,
        name='Cart_add'),
    # path('shops/',
    #     views.all_shops,
    #     name='All_Shops'),
    path('usercart/',
        views.cart_view,
        name='Cart_view'),
    path('checkout/<int:location_id>',
         views.checkout,
         name='Checkout'),
    path('update/',
         views.updateCart,
         name='updateCart'),
    path('remove/',
         views.removeItem,
         name='removeItem'),    
    #--- Add whatever you want above it --#
    ## Always keep it Last in path ###
    path('',
        views.shops_grocery,
        name='Shops_Grocery'),
    #--- Don't add any thing below this -- #
]