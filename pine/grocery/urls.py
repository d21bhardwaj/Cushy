from django.contrib import admin
from django.urls import path, include, re_path 
from django.contrib.auth import views as auth_views
from django.views.generic import RedirectView
from grocery import views 
#Login
from accounts import views as accounts_views
from django.contrib.auth import logout

urlpatterns = [    
    path('Carts/', 
        views.all_carts, 
        name='carts'),
    path('', 
        views.all_shops, 
        name='shops'),
    path('product-edit',
        views.data_upload_table,
        name='Product_Edit'),
        path('product-edit/<int:product_id>',
        views.data_upload_form,
        name='Product_Edit'),
    path('upload/',
        views.data_upload,
        name='Upload_data'),
#--- Add whatever you want above it --#
    ## Always keep it Last in path ###
    # path('',
    #     views.shops_grocery,
    #     name='Shops_Grocery'),
    #--- Don't add any thing below this -- #
]