from django.db import models

# Create your models here.

class Shop(models.Model):
    shop = models.CharField(max_length=40, null = False, default='')
    def __str__(self):
        return str(self.shop)    

class Company(models.Model):
    company  = models.CharField(max_length=40, null = False, default='') 
    # This class will be used for listing the product of the company
    def __str__(self):
        return str(self.company)
    
class Category(models.Model):
    category = models.CharField(max_length=40, null = False, default='')
    # This class will be used for listing products in sub category
    def __str__(self):
        return str(self.category)

class Product(models.Model):
    # This class will be used for listing the product company so on and so forth
    product = models.CharField(max_length=40, null = False, default='')
    quantity = models.CharField(max_length=10, null = False, default='')
    company = models.ForeignKey(Company, on_delete=models.DO_NOTHING, null = False )
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING, null = False)
    price = models.IntegerField(null = False, default='')
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, null = False )
    # off is in Rs.
    off = models.BooleanField(default=False)
    savings = models.IntegerField(null = True)