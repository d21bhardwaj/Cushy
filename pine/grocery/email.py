import json
from django.conf import settings
from accounts.models import Profile
from .models import Shop
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.shortcuts import redirect
from django.template.loader import get_template
from django.template.loader import render_to_string
from django.utils.html import strip_tags

def send_mail_order(profile,shop_id,dic,dic2):
    template = get_template('send_mail_order.html')
    profile = Profile.objects.get(id=profile)
    shop = Shop.objects.get(id=shop_id)
    location = dic2["locality"]
    context = {
            'cart':dic,
            'Name':profile.title + profile.name,
            'Mobile No.':profile.mobile_no,
            'Email':profile.email,
            'profile':profile,
            'location':location,
        }
    content = template.render(context)
    html_content = content
    subject = 'New Order by ' + str(profile.title)+' '+ str(profile.name)
    from_email, to =profile.email , shop.email
    text_content = (content)
    reply_to = profile.email
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to],[reply_to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()

def send_mail_receipt(profile,shop_id,dic,dic2):
    template = get_template('send_mail_receipt.html')
    profile = Profile.objects.get(id=profile)
    shop = Shop.objects.get(id=shop_id)
    location = dic2["locality"]
    context = {
            'cart':dic,
            'Name':profile.title + profile.name,
            'Mobile No.':profile.mobile_no,
            'Email':profile.email,
            'profile':profile,
            'shop':shop,
            'location':location,
        }
    content = template.render(context)
    html_content = content
    subject = 'Your Order List'
    from_email, to = shop.email , profile.email
    text_content = (content)
    reply_to = profile.email
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to],[reply_to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()