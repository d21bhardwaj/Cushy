from django.shortcuts import render, redirect
from .models import *
#for profile linking
from accounts.models import Profile
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required, user_passes_test
#adding for contact form

from django.contrib.auth.models import User
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.http import FileResponse
from .models import Product,Brand,Shop,Category

import openpyxl as xl


from django.shortcuts import render
from django.http import Http404
from django.http import HttpResponse
import json
from django.conf import settings

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
    product_id = request.POST.get('product_id')
    # quantity = request.POST.get('quantity')
    quantity = 2
    file_path = settings.BASE_DIR + '/static/json/user' + str(user_id) + 'cart.json'
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
            quantity = 3
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

def cart_change(request):
    user_id = request.user.pk
    product_id = request.POST.get['product_id']
    # quantity = request.POST.get['quantity']
    quantity = 1
    file_path = 'static/json/user' + str(user_id) + 'cart.json'
    with open(file_path, 'r+') as json_read:
        data = json.loads(json_read.read())
    data[str(product_id)] = quantity
    with open(file_path, 'w+') as f:
        json.dump(data, f)
    return render(request, 'page3.html')

def cart_empty(request):
    user_id = request.user.pk
    email_id = request.POST.get('email')
    file_path = 'static/json/user' + str(user_id) + 'cart.json'
    try:
        with open(file_path, 'w+') as json_new:
            d = {}
            json.dump(d, json_new)
            return render(request, 'page2.html')
    except:
        raise Http404("Action Cannot be executed!")

@user_passes_test(shop_verified, login_url='/settings/account/')
def data_upload(request):
    pk = request.user.pk
    user = User.objects.get(pk=pk)
    profile = Profile.objects.get(user=user)
    shop = Shop.objects.get(shop_user=profile)
   
    if request.method == "POST":
        excel_file = request.FILES["excel_file"]
        wb = xl.load_workbook(excel_file)
        sheet = wb.active
        # print(sheet)
        max_r = sheet.max_row
        dic = []
        for i in range(1,max_r+1): 

            if(i!=1):
                cmpe = Company.objects.filter(id=int(sheet.cell(row=i,column= 3).value)).first()
                cate = Category.objects.filter(id=int(sheet.cell(row=i,column= 4).value)).first()
                
                dic.append(Product(
                name=str(sheet.cell(row=i, column=1).value),  
                quantity=str(sheet.cell(row=i,column= 2).value), 
                brand=cmpe, 
                category=cate, 
                price=str(sheet.cell(row=i,column= 5).value),
                shop=shop,
                #off=str(sheet.cell(row=i,column= 7).value),
                savings=int(sheet.cell(row=i,column= 7).value)
                ))

        Product.objects.bulk_create(dic)
        return HttpResponse("Data created at server for"+" ")

    else:
	    return render(request,"upload_data.html")

def all_grocery(request):
    groceries = Product.objects.all()
    #print(groceries)
    return render(request, 'groceries.html', {'groceries' : groceries})

def all_shops(request):
    shops = Shop.objects.all()
    return render(request, 'shops.html',{'shops':shops})

def shops_grocery(request, shop_name):
    shop = Shop.objects.get(shop=shop_name)
    groceries = Product.objects.filter(shop=shop)

    return render(request, 'groceries.html', {'groceries' : groceries})

def all_category(request):
    category = Category.objects.all()
    
    shop_id = request.GET.get('shop',None)
    category_id = request.GET.get('category',None)
    # if shop_name is None:
    #     groceries = Products.objects.all()
    # else:
    #     groceries = Products.objects.filter(shop=shop_name)        

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
    print(user_id)
    file_path = 'static/json/user' + str(user_id) + 'cart.json'
    try:
        with open(file_path,'r+') as json_cart:
            user_cart = json.loads(json_cart.read())
            dic = {}
            for key,values in user_cart.items():
                li = []
                pro = Product.objects.filter(id=key).first()
                li.append(pro.price)
                li.append(values)
                dic[pro.product] = li

    except:
        pass

    return render(request, 'cart.html', {'cart': dic})
