from django.contrib import admin
from django.urls import path, include, re_path
from django.contrib.auth import views as auth_views
from django.views.generic import RedirectView
from grocery import views
# Login
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

    path('past-orders/', views.pastOrders, name='pastOrders'),
    path('past-orders/<int:order_num>/', views.delivered_entries, name='deliveredOrders'),
    path('deleteorderbyuser/<int:order_id>', views.deleteOrderByUser, name='deleteOrderByUser'),
    path('deleteorderbyshop/<int:order_id>', views.deleteOrderByShop, name='deleteOrderByShop'),
    path('past-orders/processed/<int:order_id>', views.makeProcessed, name='makeProcessed'),
    path('past-orders/completed/<int:order_id>', views.makeCompleted, name='makeCompleted'),
    path('past-orders/delivered/<int:order_id>', views.makeDelivered, name='makeDelivered'),

    # --- Add whatever you want above it --#
    ## Always keep it Last in path ###
    # path('',
    #     views.shops_grocery,
    #     name='Shops_Grocery'),
    # --- Don't add any thing below this -- #
]
