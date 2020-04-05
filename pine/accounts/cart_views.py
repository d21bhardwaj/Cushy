from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings
from .models import Profile
from grocery.models import Order, Shop
import json
import datetime

@login_required
def pastOrders(request):
    # id = request.user.id
    # user = Profile.objects.get(id=id)
    # orders = Order.objects.filter(user=id)
    pk = request.user.pk
    user = User.objects.get(pk=pk)
    profile = Profile.objects.get(user=user)
    orders = Order.objects.filter(user=profile).order_by('-ordered_at')
    c = 0
    order_list = []
    for order in orders:
        c += 1
        d = {'index': c}
        path = order.cart
        try :
            with open(path) as order_file:
                json_dict = json.load(order_file)
            if order.cancelled is True:
                print(path)
                try :     
                    if json_dict['cancelled_by_user'].lower() == "yes":
                        status = "Order Cancelled by user"
                    elif json_dict['cancelled_by_shop'].lower() == "yes":
                        status = "Order Cancelled by shop"
                except :
                    status = "Order Cancelled"
            else :
                if order.completed is True:
                        status = "packed"
                        try:
                            if json_dict['delivered'].lower() == "yes":
                                status = "delivered"
                        except:
                            status = "packed"
                elif order.processed is True:
                    status = "processed"
                else:
                    status = "not processed"
            print(status)
            d['status'] = status
            d['location'] = order.user.location
            try:
                d['order_amount'] = json_dict['amount']
            except :
                d['order_amount'] = "Not calculated by system"
            d['ordered_at'] = order.ordered_at
            d['shop'] = order.shop
            d['myid'] = order.id
            d['user'] = order.user
            d['order'] = order
            try:
                d['customer'] = json_dict['name']
            except :
                d['customer'] = str(order.user.title)+' '+ str(order.user.name)
            order_list.append(d)
        except:
            print("hiiii")
            continue
    if len(order_list) > 0:
        flag1 = 1
    else:
        flag1 = 0

    order_list1 = []
    if profile.shop_owner:
        try :
            shop = Shop.objects.get(shop_user=profile)
            orders = Order.objects.filter(shop=shop).order_by('-ordered_at')
            c = 0
            
            for order in orders:
                c += 1
                d = {'index': c}
                path = order.cart
                try:
                    with open(path) as order_file:
                        json_dict = json.load(order_file)
                    if order.cancelled is True:
                        try :     
                            if json_dict['cancelled_by_user'].lower() == "yes":
                                status = "Order Cancelled by user"
                            elif json_dict['cancelled_by_shop'].lower() == "yes":
                                status = "Order Cancelled by shop"
                        except :
                            status = "Order Cancelled"
                    else :
                        if order.completed is True:
                                status = "packed"
                                try:
                                    if json_dict['delivered'].lower() == "yes":
                                        status = "delivered"
                                except:
                                    status = "packed"
                        elif order.processed is True:
                            status = "processed"
                        else:
                            status = "not processed"
                    print(status)

                    d['status'] = status
                    d['location'] = order.user.location
                    try:
                        d['order_amount'] = json_dict['amount']
                    except :
                        d['order_amount'] = "Not calculated by system"
                    d['ordered_at'] = order.ordered_at
                    d['shop'] = order.shop
                    d['myid'] = order.id
                    d['order_no']=order.order_no
                    d['user'] = order.user
                    d['order'] = order
                    try:
                        d['customer'] = json_dict['name']
                    except :
                        d['customer'] = str(order.user.title)+' '+ str(order.user.name)
                    order_list1.append(d)
                except:
                    print("hiiii")
                    continue
        except :
            pass 
            
    if len(order_list1) > 0:
        flag2 = 1
        flag1 = 0
    else:
        flag2 = 0
    my_orders = True
    return render(request, 'past_orders.html', {'order_list': order_list, 'flag1': flag1, 'shop_orders': order_list1,
                                                'flag2': flag2,'my_orders':my_orders})

@login_required
def delivered_entries(request, order_num):
    id = request.user.id
    user = Profile.objects.get(id=id)
    pk = request.user.pk
    user = User.objects.get(pk=pk)
    profile = Profile.objects.get(user=user)
    shop_user = Shop.objects.get(shop_user=profile)
    try :
        orders = Order.objects.get(id=order_num,user=profile)
    except :
        orders = Order.objects.get(id=order_num,shop=shop_user)
    # orders = Order.objects.filter(user=id)
    # order_num -= 1
    order_no = orders.order_no
    path = orders.cart
    with open(path) as order_file:
        json_dict = json.load(order_file)

    order_file.close()
    ordered_prod = json_dict['orders']
    c = 0
    products = []
    for pro in ordered_prod:
        c += 1
        prod = {'index': c, 'prod_key': pro, 'ordered_prod': ordered_prod[pro],
                'amount': int(ordered_prod[pro]['Quantity']) * ordered_prod[pro]['SP']}
        products.append(prod)

    return render(request, 'delivered_orders.html', {'num': order_num , 'product': products,'order_no':order_no})

@login_required
def deleteOrderByUser(request, order_id):
    pk = request.user.pk
    user = User.objects.get(pk=pk)
    profile = Profile.objects.get(user=user)
    order = Order.objects.get(id=order_id,user=profile)

    try :
        path = order.cart
        a_file = open(path, "r")
        json_object = json.load(a_file)
        a_file.close()
        json_object['cancelled_by_user'] = "yes"
        a_file = open(path, 'w')
        json.dump(json_object, a_file)
        a_file.close()
    except :
        pass
    order.cancelled = True
    order.save()

    return redirect('pastOrders')

@login_required
def deleteOrderByShop(request, order_id):
    pk = request.user.pk
    user = User.objects.get(pk=pk)
    profile = Profile.objects.get(user=user)
    shop_user = Shop.objects.get(shop_user=profile)
    order = Order.objects.get(id=order_id,shop=shop_user)
    try :
        path = order.cart
        a_file = open(path, "r")
        json_object = json.load(a_file)
        a_file.close()
        json_object['cancelled_by_shop'] = "yes"
        a_file = open(path, 'w')
        json.dump(json_object, a_file)
        a_file.close()
    except :
        pass
    order.cancelled = True
    order.save()
    return redirect('pastOrders')

@login_required
def makeProcessed(request, order_id):
    pk = request.user.pk
    user = User.objects.get(pk=pk)
    profile = Profile.objects.get(user=user)
    shop_user = Shop.objects.get(shop_user=profile)
    order = Order.objects.get(id=order_id,shop=shop_user)
    order.processed = True
    order.save()
    return redirect('pastOrders')

@login_required
def makeCompleted(request, order_id):
    pk = request.user.pk
    user = User.objects.get(pk=pk)
    profile = Profile.objects.get(user=user)
    shop_user = Shop.objects.get(shop_user=profile)
    order = Order.objects.get(id=order_id,shop=shop_user)
    order.completed = True
    order.completed_at = datetime.datetime.now()
    order.save()
    print(order)
    return redirect('pastOrders')

@login_required
def makeDelivered(request, order_id):
    pk = request.user.pk
    user = User.objects.get(pk=pk)
    profile = Profile.objects.get(user=user)
    shop_user = Shop.objects.get(shop_user=profile)
    order = Order.objects.get(id=order_id,shop=shop_user)
    try :
        path = order.cart
        a_file = open(path, "r")
        json_object = json.load(a_file)
        a_file.close()
        json_object['delivered'] = "yes"
        a_file = open(path, 'w')
        json.dump(json_object, a_file)
        a_file.close()
    except :
        pass
    order.completed = True
    order.completed_at = datetime.datetime.now()
    order.save()
    return redirect('pastOrders')