from django.contrib import admin

# Register your models here.
from .models import Shop, Brand, Category, Product, Images

class ShopAdmin(admin.ModelAdmin):
    list_display = ('id','shop_user', 'shop','name')

class BrandAdmin(admin.ModelAdmin):
    list_display = ('id', 'brand')
    
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'category')
    
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'brand', 'price','name','quantity','shop','off','free','savings','show_product','updated_at')

class ImagesAdmin(admin.ModelAdmin):
    list_display = ('id', 'product_image', 'image')

admin.site.register(Shop, ShopAdmin)
admin.site.register(Brand, BrandAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Images, (ImagesAdmin))


