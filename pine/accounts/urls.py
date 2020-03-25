from django.urls import path, include, re_path 
from django.contrib.auth import views as auth_views
from django.views.generic import RedirectView
from accounts import views as accounts_views 
   
   
   
urlpatterns = [
      
   
   
    path('signup/', accounts_views.signup, name='signup'),
    
    path('login/', auth_views.LoginView.as_view(template_name='login.html'),name='login'),

    path('activate_account/<str:token>',accounts_views.activate_account, name='activate_account'),

    ############################################### MOBILE VERIFICATION DEMO ##################################
    
    path('otp/', accounts_views.verify_mobile, name='vm'),
#Adding url password related form the link(https://simpleisbetterthancomplex.com/series/2017/09/25/a-complete-beginners-guide-to-django-part-4.html)

    path('reset/',
        auth_views.PasswordResetView.as_view(
            template_name='password_reset.html',
            email_template_name='password_reset_email.html',
            subject_template_name='password_reset_subject.txt'),
        name='password_reset'),
    path('reset/done/',
        auth_views.PasswordResetDoneView.as_view(
            template_name='password_reset_done.html'),
        name='password_reset_done'),
    path('reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='password_reset_confirm.html'),
        name='password_reset_confirm'),
    
    path('reset/complete/',
        auth_views.PasswordResetCompleteView.as_view(
            template_name='password_reset_complete.html'),
        name='password_reset_complete'),

#Password change view
    path('settings/password/',
        auth_views.PasswordChangeView.as_view(
            template_name='password_change.html'),
        name='password_change'),
    path('settings/password/done/', 
        auth_views.PasswordChangeDoneView.as_view(
            template_name='password_change_done.html'),
        name='password_change_done'),

#MyAccount View

    path('settings/',
        accounts_views.profileupdate, 
        name='my_account'),

    path('settings/uploads',
        accounts_views.uploads,
        name='my_uploads'),
        
#Delete
    path('settings/delete/pg/<int:pg_id>/', 
        accounts_views.delete_pg, 
        name='delete_pg'),
   
    path('settings/delete/room/<int:room_id>/', 
        accounts_views.delete_room, 
        name='delete_room'),

#Hide   
    path('settings/hide/pg/<int:pg_id>/', 
        accounts_views.hide_pg, 
        name='hide_pg'),

    path('settings/hide/room/<int:room_id>/', 
        accounts_views.hide_room, 
        name='hide_room'),

#Update
    path('settings/update/room/<int:room_id>/',
        accounts_views.room_update,
        name='my_room'),

    path('settings/update/pg/<int:pg_id>/',
        accounts_views.pg_update,
        name='my_pg'),


    # path('settings/update_pic/<int:pg_id>/',
    #     accounts_views.pic_update,
    #     name='my_pics'),
    path('settings/view/room/<int:room_id>/<int:image_id>',
        accounts_views.room_view,
        name='room_view'),
    path('settings/view/pg/<int:room_id>/<int:image_id>',
        accounts_views.pg_view,
        name='pg_view'),
    path('settings/image/room/<int:room_id>',
        accounts_views.room_image,
        name='room_image'),
    path('settings/image/room/<int:room_id>/<int:image_id>',
        accounts_views.room_image_update,
        name='room_image_update'),
    path('settings/image/pg/<int:room_id>',
        accounts_views.pg_image,
        name='pg_image'),
    path('settings/image/pg/<int:room_id>/<int:image_id>',
        accounts_views.pg_image_update,
        name='pg_image_update'),
]