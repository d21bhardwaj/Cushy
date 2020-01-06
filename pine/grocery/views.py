from django.shortcuts import render, redirect
from .models import *
#for profile linking
from accounts.models import Profile
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required, user_passes_test
#adding for contact form
from main.models import Location
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.http import FileResponse
from .models import Product,Brand,Shop,Category
from .forms import *
import openpyxl as xl
from .email import *
from django.shortcuts import render
from django.http import Http404
from django.http import HttpResponse
import json
from django.conf import settings
import logging
import os
import time
import shutil

logging.basicConfig( filename="media/grocery.log", level=logging.WARNING)

def user_verified(user):
    try:
        return user.profile.is_verified()
    except ObjectDoesNotExist:
        return False

def shop_verified(user):
    try:
        return user.profile.is_shop_owner()
    except ObjectDoesNotExist:
        return False

@user_passes_test(user_verified, login_url='/settings/account/')
def cart_add(request):
    user_id = request.user.pk
    profile = Profile.objects.get(user = user_id)
    product_id = request.POST.get('product_id')
    quantity = 1
    file_path = settings.BASE_DIR + '/media/json/active/user' + str(profile.id) + 'cart.json'
    try:
        with open(file_path, 'r') as json_read:
            data = json.loads(json_read.read())
        try:
            if(data[str(product_id)] >= 0):
                data[str(product_id)] += quantity
        except:
            data[str(product_id)] = quantity
        with open(file_path, 'w+') as f:
            json.dump(data, f)
    except:
        with open(file_path, 'w+') as json_file:
            add = {}
            quantity = 1
            add[str(product_id)] = quantity
            json.dump(add, json_file)
    return render(request, 'cart.html')

@user_passes_test(user_verified, login_url='/settings/account/')
def show_savings(cart):
    total_savings = 0
    for product in cart.keys():
        prod_obj = Product.objects.get(id = product)
        total_savings = total_savings + cart[product]*(prod_obj.off)
    return total_savings

@user_passes_test(user_verified, login_url='/settings/account/')
def updateCart(request):
    user_id = request.user.pk
    profile = Profile.objects.get(user = user_id)
    product_id = request.POST.get('product_id')
    quantity = request.POST.get('quantity')
    print(product_id,quantity)
    file_path = 'media/json/active/user' + str(profile.id) + 'cart.json'
    with open(file_path, 'r+') as json_read:
        data = json.loads(json_read.read())
    data[str(product_id)] = quantity
    with open(file_path, 'w+') as f:
        json.dump(data, f)
    return render(request, 'cart.html', {'cart': data})

@user_passes_test(user_verified, login_url='/settings/account/')
def cart_empty(request):
    user_id = request.user.pk
    profile = Profile.objects.get(user = user_id)
    email_id = request.POST.get('email')
    file_path = 'media/json/active/user' + str(profile.id) + 'cart.json'
    try:
        with open(file_path, 'w+') as json_new:
            d = {}
            json.dump(d, json_new)
            return render(request, 'page2.html')
    except:
        #raise Http404("Action Cannot be executed!")
        pass

@user_passes_test(shop_verified, login_url='/settings/account/')
def data_upload(request):
    pk = request.user.pk
    user = User.objects.get(pk=pk)
    profile = Profile.objects.get(user=user)
    shop_user = Shop.objects.get(shop_user=profile)
   
    if request.method == "POST":
        excel_file = request.FILES["excel_file"]
        wb = xl.load_workbook(excel_file)
        sheet = wb.active
        # print(sheet)
        max_r = sheet.max_row
        dic = []
        for i in range(1,max_r+1): 
            if(i!=1): 
                name          = str(sheet.cell(row=i,column=2).value),
                quantity      = str(sheet.cell(row=i,column=3).value),
                price         = int(sheet.cell(row=i,column=4).value),  
                selling_price = int(sheet.cell(row=i,column=5).value), 
                description   = str(sheet.cell(row=i,column=6).value), 
                #barcode       = str(sheet.cell(row=i,column=7).value),
                
                off = False
                if price != selling_price :
                    off = True
                    savings = price[0] - selling_price[0]
                    print(savings)
                else :
                    savings = 0             
                dic.append(Product(
                #id            = str(sheet.cell(row=i,column=1).value),      
                name          = str(sheet.cell(row=i,column=2).value),
                quantity      = str(sheet.cell(row=i,column=3).value),
                price         = str(sheet.cell(row=i,column=4).value),  
                selling_price = str(sheet.cell(row=i,column=5).value), 
                description   = str(sheet.cell(row=i,column=6).value), 
                #barcode       = str(sheet.cell(row=i,column=7).value),
                shop          = shop_user, 
                off           = str(off),
                savings       = str(savings),
                ))
                print(shop_user)        
        Product.objects.bulk_create(dic)
        return HttpResponse("Data created at server for"+" ")


        Product.objects.bulk_create(dic)
        return HttpResponse("Data created at server for"+" ")

    else:
        return render(request,"upload_data.html")

@user_passes_test(shop_verified, login_url='/settings/account/')
def data_upload_table(request):
    pk = request.user.pk
    user = User.objects.get(pk=pk)
    profile = Profile.objects.get(user=user)
    shop = Shop.objects.get(shop_user=profile)
    groceries = Product.objects.filter(shop=shop)
    
    return render(request, 'grocery_list_edit.html', {'groceries' : groceries, 'form':'form'})
    
        

@user_passes_test(shop_verified, login_url='/settings/account/')
def data_upload_form(request, product_id):
    pk = request.user.pk
    user = User.objects.get(pk=pk)
    profile = Profile.objects.get(user=user)
    shop = Shop.objects.get(shop_user=profile)
    groceries = Product.objects.filter(shop=shop)
    items = Product.objects.get(id=product_id)
    form_class = ProductForm(shop,instance=items)
    images = Images.objects.filter(product_image=product_id).first()
    imageform = ImageForm(instance=images)
    if request.method == 'POST': 
        form = ProductForm(shop, request.POST,instance=items)
        # if images is not None :
        #     imageform = ImageForm(request.POST, request.FILES, instance=images)
        # else :
        imageform = ImageForm(request.POST, request.FILES)
        if form.is_valid() and imageform.is_valid():
            post_form = form.save(commit=False)
            post_form.shop = shop
            post_form.instance = items
            
            post_form.save()
            if images is not None :
                photo = Images(id= images.id, product_image=post_form, image= imageform.instance.image)
            else :
                photo = Images(product_image=post_form, image= imageform.instance.image)
            if imageform.cleaned_data['image']:
                photo.save()
            return redirect('Product_Edit')
        else:
            print(form.errors, imageform.errors)
    else :
        form = form_class   
    return render(request, 'grocery_list_edit.html', {'product_id':product_id,'groceries':groceries, 'form':form,'imageform':imageform})



def all_grocery(request):
    groceries = Product.objects.all()
    dic = {}
    user_id = request.user.pk
    profile = Profile.objects.get(user = user_id)
    if request.user.is_authenticated:
        file_path = 'media/json/active/user' + str(profile.id) + 'cart.json'
        try:
            with open(file_path,'r+') as json_cart:
                user_cart = json.loads(json_cart.read())
                for key,values in user_cart.items():
                    dic[key] = values
                print(file_path)
        except:
            print("fuck")
    else:
        print("no")
    print(dic)
    return render(request, 'groceries.html', {'groceries': groceries, 'dic': dic})

def all_shops(request):
    shops = Shop.objects.all()
    return render(request, 'shops.html',{'shops':shops})

def request_url(request):
    S = request.path 
    S = ((S.split('/'))[1].split('/')[0])
    return str(S)

def shops_grocery(request):
    shop_name = request_url(request)
    shop = Shop.objects.get(shop=shop_name)
    groceries = Product.objects.filter(shop=shop,show_product=True)
    user_id = request.user.pk
    profile = Profile.objects.get(user = user_id)
    dic = []
    if request.user.is_authenticated:
        file_path = 'media/json/active/user' + str(profile.id) + 'cart.json'
        try:
            with open(file_path,'r+') as json_cart:
                user_cart = json.loads(json_cart.read())
                for key,values in user_cart.items():
                    dic.append(int(key))
        except:
            print("Error1")
    else:
        print("Error2")
    print(dic)

    return render(request, 'groceries.html', {'groceries' : groceries,'shop_name':shop_name , 'dic':dic})

def all_category(request):
    category = Category.objects.all()
    shop_id = request.GET.get('shop',None)
    category_id = request.GET.get('category',None)  

    return render(request, '#',{'category':category})

def category_grocery(request, shop_name, category_name):
    shop = Shops.objects.get(shop=shop_name)
    category = Category.objects.filter(category=category_name)
    groceries = Products.objects.filter(shop=shop,category=category)

    return render(request, 'groceries.html', {'groceries' : groceries})

def all_brands(request):
    brand = Brand.objects.all()
    groceries = Products.objects.filter(brand=brand)
    return render(request, '#',{'brands':brands})

def all_brands(request, shop_name, brand_name):
    shop = Shops.objects.get(shop=shop_name)
    category = Category.objects.filter(category=category_name)
    groceries = Products.objects.filter(shop=shop,category=category)

    return render(request, 'groceries.html', {'groceries' : groceries})

@user_passes_test(user_verified, login_url='/settings/account/')
def cart_view(request):
    user_id = request.user.pk
    profile = Profile.objects.get(user=user_id)
    
    file_path = 'media/json/active/user' + str(profile.id) + 'cart.json'
    location_id =request.POST.get('location')
    if(request.POST):
        print(location_id)
        return redirect('Checkout', location_id)
    try:
        with open(file_path,'r+') as json_cart:
            user_cart = json.loads(json_cart.read())
            dic = {}
            for key,values in user_cart.items():
                li = []
                pro = Product.objects.filter(id=key).first()
                try:
                    im = Images.objects.filter(product_image=key).first()
                    imn = im.image.url
                except:
                    imn = "/static/assets/img/no-image.png"
                li.append(pro.price)
                li.append(values)
                li.append(pro.name)
                li.append(imn)
                li.append(pro.selling_price)
                li.append(pro.savings)
                dic[key] = li
    except:
        return render(request, 'cart.html', {'cart': {}})
    form = DeliveryLocationForm()
    return render(request, 'cart.html', {'cart': dic,'profile':profile,'form':form})

@user_passes_test(user_verified, login_url='/settings/account/')
def removeItem(request):
    user_id = request.user.pk
    profile = Profile.objects.get(user = user_id)
    file_path = 'media/json/active/user' + str(profile.id) + 'cart.json'
    product_id = request.POST.get('product_id')
    print(request.POST.get)
    with open(file_path, 'r') as json_cart:
        user_cart = json.loads(json_cart.read())
    del user_cart[str(product_id)]
    with open(file_path, 'w+') as json_cart:
        json.dump(user_cart, json_cart)
    print(user_cart)
    return render(request, 'cart.html', {'cart': user_cart})

@user_passes_test(user_verified, login_url='/settings/account/')
def checkout(request,location_id):
    user_id = request.user.pk
    profile = Profile.objects.get(user = user_id)
    file_path = 'media/json/active/user' + str(profile.id) + 'cart.json'
    dic2 = {}
    print(request.POST)
    location = Location.objects.get(id=location_id)
    try:
        with open(file_path, 'r+') as json_cart:
            dic = {}
            user_cart = json.loads(json_cart.read())
            for key, value in user_cart.items():
                li = []
                pro = Product.objects.filter(id=key).first()
                try:
                    im = Images.objects.filter(product_image=key).first()
                    imn = im.image.url
                except:
                    imn = "/static/assets/img/no-image.png"
                li.append(pro.name) #0            
                li.append(pro.price) #1
                li.append(pro.selling_price) #2
                li.append(value) #3 ----"Quantity order" ----- #
                li.append(imn)   #4
                li.append(pro.shop.shop)  #5
                dic[key] = li  #6
            shopName = pro.shop.id
    except:
        return Http404
    try:
        user_name = profile.title + profile.name
        details = []
        details.append(dic)
        details.append(profile.mobile_no)
        details.append(profile.email)
        dic2[user_name] = details
        local = []
        local.append(location.location)
        dic2['locality'] = local
    except:
        pass
    # function to send mail
    file_path1 = 'media/json/user_' + str(profile.id) + '/' + 'shop_' + str(time.strftime('%Y-%m-%d--%H-%M-%S')) + '_' + str(shopName) + 'Cart.json'
    file_path2 = 'media/json/shop_' + str(shopName) + '/' + 'user_' + str(time.strftime('%Y-%m-%d--%H-%M-%S')) + '_' + str(profile.id) + 'Cart.json'

    try:
        os.mkdir('media/json/shop_' + str(shopName))
        os.mkdir('media/json/user_' + str(profile.id))
    except:
        pass

    try:
        with open(file_path1, 'a+') as json_file:
            json.dump(dic,json_file)
    except:
        pass

    try:
        with open(file_path2, 'a+') as json_file:
            json.dump(dic2,json_file)
    except:
        pass
    send_mail_order(profile.id,shopName,dic,dic2)
    
    open(file_path, 'w').close()

    return redirect('/')



