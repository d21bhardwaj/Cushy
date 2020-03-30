from django.contrib import admin
from .models import RentingUser, RentingPGUser, Images, ImagesPG, Location

class RentingUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_profile','created_at','updated_at','approved','hidden','hidden_at')

class RentingPGUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_profile','created_at','updated_at','approved','hidden','hidden_at')

admin.site.register(RentingUser, RentingUserAdmin)
admin.site.register(RentingPGUser, RentingPGUserAdmin)
admin.site.register(Images)
admin.site.register(ImagesPG)
admin.site.register(Location)

