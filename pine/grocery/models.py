from django.db import models
from django.contrib.auth.models import User
from accounts.models import Profile
from django.db.models.signals import pre_save
from django.utils.timezone import now
import time
from django.template.defaultfilters import slugify

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
    shop = models.SlugField(max_length=40,  default='')
    mobile_no = models.CharField(null=True,blank=True,max_length=12)
    alternate_no = models.CharField(null=True,blank=True,max_length=12)
    email = models.EmailField(max_length=70, null=True, blank=True)
    image = models.ImageField(upload_to=shop_directory_path, validators=[validate_image],verbose_name='Shop Image',null=True)
    name = models.CharField(max_length=40, unique=True) 
    description = models.CharField(null=True,blank=True,max_length=200) 
    cart_message = models.CharField(null=True,blank=True,max_length=200)
    location = models.ForeignKey('main.Location',on_delete=models.SET_NULL,null=True)
    delivery = models.BooleanField(default=False)
    delivery_at = models.ManyToManyField('main.Location',related_name='delivery_available_at', blank=True)
    taking_orders = models.BooleanField(default=False)
    opening_time = models.DateTimeField(null=True, blank=True)
    closing_time = models.DateTimeField(null=True, blank=True)
    minimum_order = models.IntegerField(null=True, blank=True)
    def save(self, *args, **kwargs):
        self.shop = slugify(self.name)

        super(Shop, self).save(*args, **kwargs)   

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
    selling_price = models.IntegerField(null = False,blank= False)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, null = False )
    off = models.BooleanField(default=False)
    free = models.BooleanField(default=False)
    free_product = models.ForeignKey('self',on_delete=models.SET_NULL,null = True, blank = True)
    description = models.TextField(max_length=100, blank=True, null = True)
    savings = models.IntegerField(null = True, blank= True)
    barcode = models.IntegerField(null = True, blank= True)        
    show_product = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True, blank=True)
    maximum_cap = models.IntegerField(null=True,blank=True)
    def __str__(self):
        return str(self.name)

class Images(models.Model):
    product_image = models.ForeignKey(Product, default=None, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=product_directory_path, validators=[validate_image],verbose_name='Product Image')

    def __str__(self):
        return str(self.image)


def complete_info(sender, **kwargs): 
    product = kwargs["instance"]
    if product.off is False:   
        if product.price != product.selling_price:
            product.off = True
            product.savings = product.price - product.selling_price
    if product.free is False:
        if product.free_product is not None:
            product.free = True
    if product.free_product is None:
        product.free = False
    if product.price == product.selling_price:
        product.off = False
    if product.price != product.selling_price:
            product.off = True
            product.savings = product.price - product.selling_price

pre_save.connect(complete_info, sender=Product)      

class Order(models.Model):
    order_no = models.CharField(unique=True,max_length=100)
    shop = models.ForeignKey(Shop, on_delete=models.DO_NOTHING)
    user = models.ForeignKey('accounts.Profile', on_delete=models.DO_NOTHING)
    cart = models.FilePathField(path='media/json',match='/*.json$',recursive=True)
    processed = models.BooleanField(default=False)
    completed = models.BooleanField(default=False)
    ordered_at = models.DateTimeField(default=now, blank=True)
    completed_at = models.DateTimeField(default=now, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['user','ordered_at']),
            models.Index(fields=['shop', 'ordered_at',]),
        ]
    def save(self, *args, **kwargs):
        super(Order, self).save(*args, **kwargs)
        shop = self.shop
        user = self.user
        print(self.id)
        self.order_no = str(shop.location.city.id)+'/'+ str(shop.location.id)+'/'+str(user.id)+'/'+ str(shop.id)+'/'+str(self.id)
        super(Order, self).save(*args, **kwargs)
                    
