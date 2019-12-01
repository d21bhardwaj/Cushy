from django.contrib import admin

# Register your models here.
from .models import Shop, Brand, Category, Product

class ShopAdmin(admin.ModelAdmin):
    list_display = ('id', 'shop')

class BrandAdmin(admin.ModelAdmin):
    list_display = ('id', 'brand')
    
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'category')
    
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'brand', 'category','price','product','quantity','shop','off','savings')

admin.site.register(Shop, ShopAdmin)
admin.site.register(Brand, BrandAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)


