from django.contrib import admin
from .models import Profile
# Register your models here.

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'name','mobile_no','email','verified')
    

admin.site.register(Profile, ProfileAdmin)