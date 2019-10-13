from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.forms import modelformset_factory

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

import xlrd as xl

def data_upload(request,token):

	if request.method == "POST":

		excel_file = request.FILES["excel_file"]
        wb = xl.open_workbook(excel_file)
        sheet = wb.sheet_by_index(0)
        dic = []
        for i in range(sheet.nrows): 

            if(i!=0):
                dic.append(Product(product=str(sheet.cell_value(i, 1))  ,mobile=str(sheet.cell_value(i, 2)) ,bib=str(sheet.cell_value(i, 3)) , age=str(sheet.cell_value(i, 4)) , gender=str(sheet.cell_value(i, 5))))

        Product.objects.bulk_create(dic)

	    return HttpResponse("Data created at server for"+" "+str(token))

	else:
		return render(request,"data_upload.html")


