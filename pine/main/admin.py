from django.contrib import admin
from .models import RentingUser, RentingPGUser, Images, ImagesPG, Location

class RentingUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_profile','created_at','updated_at','approved','hidden','hidden_at')

class RentingPGUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_profile','created_at','updated_at','approved','hidden','hidden_at')

class ImagesUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'user','image')

class ImagesPGUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'user','image')
    
admin.site.register(RentingUser, RentingUserAdmin)
admin.site.register(RentingPGUser, RentingPGUserAdmin)
admin.site.register(Images, ImagesUserAdmin)
admin.site.register(ImagesPG, ImagesPGUserAdmin)
admin.site.register(Location)

