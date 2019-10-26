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

   