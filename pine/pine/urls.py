"""pine URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path 
from django.contrib.auth import views as auth_views
from django.views.generic import RedirectView
from main import views
from grocery import views as grocery_view
#Login
from django.contrib.auth import logout
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.models import User
#from accounts import rest_views
#from rest_framework import routers

#router = routers.DefaultRouter()
#router.register(r'users', rest_views.UserViewSet)
#router.register(r'groups', rest_views.GroupViewSet)


urlpatterns = [
    path('dashtown/', admin.site.urls),
    path('',include('main.urls')),
    path('Grocery/', include('grocery.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/profile/', RedirectView.as_view(pattern_name='index', permanent=False)),
    path('', views.index, name='index'),
    path('account/',include('accounts.urls')),
#    path('', include(router.urls)),
#    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('<shopname>/<int:shop_location>/',include('grocery.shop_urls')),
    path('<shopname>/', grocery_view.shops_by_name),
    # path('Test_Shop/',include('grocery.shop_urls')),  
]
    
if settings.DEBUG is True:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
