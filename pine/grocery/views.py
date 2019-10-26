from django.shortcuts import render, redirect
from .models import Product
#for profile linking
from accounts.models import Profile
from django.core.exceptions import PermissionDenied


#adding for contact form
from django.core.mail import EmailMessage
from django.shortcuts import redirect
from django.template.loader import get_template
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.http import FileResponse
from .models import Product,Company,Shop,Category

import openpyxl as xl

def data_upload(request):
    if request.method == "POST":
        excel_file = request.FILES["excel_file"]
        wb = xl.load_workbook(excel_file)
        sheet = wb.active
        # print(sheet)
        max_r = sheet.max_row
# from django.shortcuts import render, redirect
# from django.contrib.auth import logout
# from django.forms import modelformset_factory
#
# #for profile linking
# from accounts.models import Profile
# from django.core.exceptions import PermissionDenied
#
# #adding for contact form
# from django.core.mail import EmailMessage
# from django.shortcuts import redirect
# from django.template.loader import get_template
# from django.contrib.auth.decorators import login_required, user_passes_test
# from django.contrib.auth.models import User
# from django.contrib import messages
# from django.core.exceptions import ObjectDoesNotExist
# from django.http import FileResponse
from .models import Product,Company,Shop,Category
import xlrd as xl
from django.shortcuts import render
from django.http import Http404
import json
from django.conf import settings

def cart_add(request):
    user_id = request.user.pk
    product_id = request.POST.get('product_id')
    quantity = 2
    new_item = []
    new_item.append({str(product_id):quantity})
    file_path = settings.BASE_DIR + '/static/json/user' + str(user_id) + 'cart.json'
    try:
        with open(file_path, 'r+') as json_read:
            data = json.loads(json_read.read())
        data[str(user_id)].extend(add)
        with open(file_path, 'w+') as f:
            json.dump(data, f)
    except:
        with open(file_path, 'w+') as json_file:
            d = {}
            quantity = 3;
            d[str(product_id)] = 3
            json.dump(d, json_file)
    return render(request, 'groceries.html')


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
    file_path = 'static/json/user' + str(user_id) + 'cart.json'
    with open(file_path, 'r+') as json_read:
        data = json.loads(json_read.read())
    data[product_id] = 1
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




def data_upload(request,token):
    if request.method == "POST":

        excel_file = request.FILES["excel_file"]
        wb = xl.open_workbook(excel_file)
        sheet = wb.sheet_by_index(0)
        dic = []
        for i in range(1,max_r+1): 

            if(i!=1):
                cmpe = Company.objects.filter(id=int(sheet.cell(row=i,column= 3).value)).first()
                cate = Category.objects.filter(id=int(sheet.cell(row=i,column= 4).value)).first()
                sh = Shop.objects.filter(id=int(sheet.cell(row=i,column= 6).value)).first()
                dic.append(Product(
                product=str(sheet.cell(row=i, column=1).value),  
                quantity=str(sheet.cell(row=i,column= 2).value), 
                company=cmpe, 
                category=cate, 
                price=str(sheet.cell(row=i,column= 5).value),
                shop=sh,
                #off=str(sheet.cell(row=i,column= 7).value),
                savings=int(sheet.cell(row=i,column= 7).value)
                ))

        Product.objects.bulk_create(dic)
        return HttpResponse("Data created at server for"+" "+str(token))

    else:
	    return render(request,"upload_data.html")


def all_grocery(request):
    groceries = Product.objects.all()
    print(groceries)
    return render(request, 'groceries.html', {'groceries' : groceries})

   