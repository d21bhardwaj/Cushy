from django.contrib import admin
from .models import RentingUser, RentingPGUser, Images, ImagesPG

admin.site.register(RentingUser)
admin.site.register(RentingPGUser)
admin.site.register(Images)
admin.site.register(ImagesPG)

