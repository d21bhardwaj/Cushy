from django.db import models
from django.contrib.auth.models import User
from accounts.models import Profile
from django.db.models.signals import pre_save

# Create your models here.
def shop_directory_path(instance, filename):
    seller = instance.shop_user
    
    return 'Grocery/{id}/{file}'.format(id=seller, file = filename)
    #return 'Images/user_{0}/{1}'.format(instance.user.id, filename)

def validate_image(fieldfile_obj):
    filesize = fieldfile_obj.file.size
    megabyte_limit = 2.0
    if filesize > megabyte_limit*1024*1024:
        raise ValidationError('File size must be under 2MB. Current file size is %.2fMB.' %  (filesize/1024/1024))

# Product Code (or SKU), Product Name, Description, Category, Selling Price, Discount (If any) Brand, Colour and other applicable attributes.

def category_directory_path(instance, filename):
    category = instance.category
    
    return 'Grocery/{id}/{file}'.format(id=category, file = filename)

def brand_directory_path(instance, filename):
    brand = instance.brand

    return 'Grocery/{id}/{file}'.format(id=brand, file = filename)

def product_directory_path(instance, filename):
    seller = instance.product_image.shop
    
    return 'Grocery/{id}/{file}'.format(id=seller, file = filename)

class Shop(models.Model):
    
    shop_user = models.ForeignKey(Profile, on_delete=models.CASCADE, default='',null = True)
    shop = models.CharField(max_length=40, null = False, default='')
    mobile_no = models.CharField(null=True,blank=True,max_length=12)
    alternate_no = models.CharField(null=True,blank=True,max_length=12)
    email = models.EmailField(max_length=70, null=True, blank=True)
    image = models.ImageField(upload_to=shop_directory_path, validators=[validate_image],verbose_name='Shop Image',null=True)
    
    def __str__(self):
        return str(self.shop)    

class Brand(models.Model):
    brand  = models.CharField(max_length=40, null = False, default='') 
    image = models.ImageField(upload_to=brand_directory_path, validators=[validate_image],verbose_name='Brand Image', null=True)
    # This class will be used for listing the product of the company
    def __str__(self):
        return str(self.brand)
    
class Category(models.Model):
    category = models.CharField(max_length=40, null = False, default='')
    image = models.ImageField(upload_to=category_directory_path, validators=[validate_image],verbose_name='Category Image',null=True)
    # This class will be used for listing products in sub category
    def __str__(self):
        return str(self.category)


class Product(models.Model): 
    # This class will be used for listing the product company so on and so forth
    name = models.CharField(max_length=40, null = False, default='')
    quantity = models.CharField(max_length=10, null = False, default='')
    brand = models.ForeignKey(Brand, on_delete=models.DO_NOTHING, null = True, blank=True )
    category = models.ManyToManyField(Category, blank=True)
    price = models.IntegerField(null = False, blank= False, default='')
    selling_price = models.IntegerField(null = False,blank= False, default='')
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, null = False )
    barcode = models.IntegerField(null = True, blank= True)
    off = models.BooleanField()
    free = models.BooleanField(default=False)
    free_product = models.ForeignKey('self',on_delete=models.SET_NULL,null = True, blank = True)
    description = models.TextField(max_length=100, blank=True, null = True)
    savings = models.IntegerField(null = True, blank= True)
    barcode = models.IntegerField(null = True, blank= True)
    
    def __str__(self):
        return str(self.name)

class Images(models.Model):
    product_image = models.ForeignKey(Product, default=None, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=product_directory_path, validators=[validate_image],verbose_name='Product Image')

    def __str__(self):
        return str(self.image)


def complete_info(sender, **kwargs): 
    product = kwargs["instance"]
    print(product)
    print(product.off)
    print(kwargs["update_fields"])
    print(product.free_product)

    if product.off is False:
        print(1)
        if product.price != product.selling_price:
            product.off = True
            print(product.off)
            print(product.price)
            print(product.selling_price)
            product.savings = product.price - product.selling_price
    if product.free is False:
        if product.free_product is not None:
            product.free = True
    if product.free_product is None:
        product.free = False
    if product.price == product.selling_price:
        product.off = False
       
    
pre_save.connect(complete_info, sender=Product)      

