from django.contrib import admin

# Register your models here.
from .models import Shop, Company, Category, Product

class ShopAdmin(admin.ModelAdmin):
    list_display = ('id', 'shop')

class CompanyAdmin(admin.ModelAdmin):
    list_display = ('id', 'company')
    
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'category')
    
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'brand', 'category','price','product','quantity','shop','off','savings')

admin.site.register(Shop, ShopAdmin)
admin.site.register(Company, CompanyAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)


