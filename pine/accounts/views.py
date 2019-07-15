from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login
from django.http import HttpResponse, JsonResponse
#from django.contrib.auth.forms import UserCreationForm Not needed now
from .forms import SignUpForm, ProfileForm
# Now adding for Account View
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
# not required i guess(d) from django.views.generic import UpdateView
from django.contrib.auth.forms import PasswordChangeForm, AdminPasswordChangeForm

from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from social_django.models import UserSocialAuth

#for profile update view
from django.views.generic.edit import UpdateView
from .models import Profile
from django.forms.models import inlineformset_factory
from django.core.exceptions import PermissionDenied
from django.core.mail import EmailMessage
#for mobile verification
from .mobile_verification import *
from .function import *
from .token import *
from django.template.loader import render_to_string,get_template
# Create your views here.

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            # login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            auth_login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('index')
    else:
        form = SignUpForm()
    return render(request, 'signup.html',{'form': form , 'header':'Sign Up'})


#My account view

@login_required
def profileupdate(request):
    pk = request.user.pk
    user = User.objects.get(pk=pk)
    user_form = ProfileForm(instance=user)
 
    ProfileInlineFormset = inlineformset_factory( User, model=Profile, form=ProfileForm, can_delete=False)
    formset = ProfileInlineFormset(instance=user)
 
    if request.user.is_authenticated and request.user.id == user.id:
        if request.method == "POST":
            user_form = ProfileForm(request.POST, request.FILES, instance=user)
            formset = ProfileInlineFormset(request.POST, request.FILES, instance=user)
 
            if user_form.is_valid():
                created_user = user_form.save(commit=False)
                formset = ProfileInlineFormset(request.POST, request.FILES, instance=created_user)
 
                if formset.is_valid():
                    created_user.save()
                    formset.save()
                    ##########################################
                    usr = Profile.objects.filter(user=request.user).first()
                    usr.session_id  = otp_send(request.POST['profile-0-mobile_no'])
                    usr.save()
                    mail = request.POST['profile-0-email']
                    usr = Profile.objects.filter(user_id=request.user.id).first()
                    template = get_template('email_ver.txt')
                    context = {
                    "name" : usr.name,
                    "link": "https://pinetown.in/activate_account/"+encrypt_val(str(usr.id)+";"+usr.name),
                    
                    }
                    content = template.render(context)
                    email = EmailMessage(
                        "Email Verification",
                        content,
                        "CushyRooms" +'',
                        [mail],
                        headers = {'Reply-To': 'project.pinetown@gmail.com' }
                    )
                    email.send()
                    return redirect('/otp/')
                else:
 
                    return render(request, 'my_account.html', {
                        "noodle": pk,
                        "noodle_form": user_form,
                        "formset": formset,
                        })
            else:
 
                return render(request, 'my_account.html', {
                    "noodle": pk,
                    "noodle_form": user_form,
                    "formset": formset,
                    })
        else:
 
            return render(request, 'my_account.html', {
                "noodle": pk,
                "noodle_form": user_form,
                "formset": formset,
                'header':'Profile Update'})
    else:
        raise PermissionDenied


@login_required
def password(request):
    if request.user.has_usable_password():
        PasswordForm = PasswordChangeForm
    else:
        PasswordForm = AdminPasswordChangeForm

    if request.method == 'POST':
        form = PasswordForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordForm(request.user)
    return render(request, 'my_account.html', {'form': form })


def verify_mobile(request):
    if request.method == "POST":
        user = Profile.objects.filter(user_id = request.user.id).first()
        user.verified = False
        otp = request.POST['otp']
        resp = otp_recieve(user.session_id,otp)
        
        if resp == "OTP Matched":
            user.verified = True
            user.save()
            return render(request, 'verified.html')
        else:
            return render(request, 'not_verified.html')
    return render(request, 'otp.html',{'header':'Mobile Number Verification'})

def activate_account(request,token):
    token = decrypt_val(token)
    iden = int(token.split(";")[0])
    usr = Profile.objects.filter(id=iden).first()
    usr.email_verified = True
    usr.save()
    return redirect("/")
