from django.shortcuts import render, redirect
from .models import Product
#for profile linking
from accounts.models import Profile
from django.core.exceptions import PermissionDenied



import xlrd as xl

# def data_upload(request,token):

# 	if request.method == "POST":

# 		excel_file = request.FILES["excel_file"]
#         wb = xl.open_workbook(excel_file)
#         sheet = wb.sheet_by_index(0)
#         dic = []
#         for i in range(sheet.nrows): 

#             if(i!=0):
#                 dic.append(Product(product=str(sheet.cell_value(i, 1))  ,mobile=str(sheet.cell_value(i, 2)) ,bib=str(sheet.cell_value(i, 3)) , age=str(sheet.cell_value(i, 4)) , gender=str(sheet.cell_value(i, 5))))

#         Product.objects.bulk_create(dic)

# 	    return HttpResponse("Data created at server for"+" "+str(token))

# 	else:
# 		return render(request,"data_upload.html")


def all_grocery(request):

    items = Product.objects.all()
    return render(request, 'all_grocery.html', {'items':items})
