from urllib import request

from django import template

from grocery.models import *

register = template.Library()


@register.inclusion_tag('links.html')
def user_has_shop(user):
    links = [{'id': 'pastOrders', 'value': "Your Past Orders"}]
    pk = user.pk
    user = User.objects.get(pk=pk)
    try:
        a = Profile.objects.get(user=user)
        b = Shop.objects.get(shop_user=a)
        links.append({'id': 'shopOrders', 'value': "Past Shop Orders"})
    except:
        pass
    return {'links': links}


@register.inclusion_tag('three_or_four.html')
def three_or_four(user):
    pk = user.pk
    user = User.objects.get(pk=pk)
    try:
        a = Profile.objects.get(user=user)
        b = Shop.objects.get(shop_user=a)
        links = [
            {'id': 'my_account', 'value': "Edit Profile", 'name': "my_profile"},
            {'id': 'pastOrders', 'value': "Your Orders", 'name': "my_orders"},
            {'id': 'shopOrders', 'value': "Your Shop Orders", 'name': "my_shop_orders"},
            {'id': 'contact_us', 'value': "Contact Us", 'name': "not_given"}
        ]
        return {'links': links, 'space': 3}
    except:
        links = [
            {'id': 'my_account', 'value': "Edit Profile", 'name': "my_profile"},
            {'id': 'pastOrders', 'value': "Your Orders", 'name': "my_orders"},
            {'id': 'contact_us', 'value': "Contact Us", 'name': "not_given"}
        ]
        return {'links': links, 'space': 4}
