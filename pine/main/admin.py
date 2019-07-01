from django.contrib import admin
from .models import RentingUser, RentingPGUser, Images, ImagesPG

class RentingUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_profile','updated_at','approved')

class RentingPGUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_profile','updated_at','approved')

admin.site.register(RentingUser, RentingUserAdmin)
admin.site.register(RentingPGUser, RentingPGUserAdmin)
admin.site.register(Images)
admin.site.register(ImagesPG)

