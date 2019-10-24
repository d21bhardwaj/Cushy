from django.shortcuts import render
from django.http import Http404
import json

def cart_add(request,product_id,quantity):
    user_id = request.user.pk
    new_item = []
    new_item.append({str(product_id):quantity})
    file_path = 'static/json/user' + str(user_id) + 'cart.json'
    try:
        with open(file_path, 'r+') as json_read:
            data = json.loads(json_read.read())
        data[str(user_id)].extend(add)
        with open(file_path, 'a+') as f:
            json.dump(data, f)
    except:
        with open(file_path, 'a+') as json_file:
            d = {}
            d[str(user_id)] = []
            d[str(user_id)].extend(add)
            json.dump(d, json_file)
    return render(request, 'page.html')


def cart_empty(request):
    user_id = request.user.pk
    file_path = 'static/json/user' + str(user_id) + 'cart.json'
    try:
        with open(file_path, 'w+') as json_new:
            d = {}
            json.dump(d, json_new)
            return render(request, 'page2.html')
    except:
        raise Http404("Action Cannot be executed!")