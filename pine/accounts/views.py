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
#change 1
from django.forms.models import modelformset_factory
from django.core.exceptions import PermissionDenied
from django.core.mail import EmailMessage
from django.core.exceptions import ObjectDoesNotExist

#for all the uploads done by an user
from main.models import RentingUser, RentingPGUser, ImagesPG, Images
from main.forms import RentForm, RentPGForm, ImageFormPG, ImageForm
#for mobile verification
from .mobile_verification import *
from .function import *
from .token import *
from django.template.loader import render_to_string,get_template
# time stamp
from django.utils import timezone
import datetime
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
 
                    return render(request, 'my_profile.html', {
                        "noodle": pk,
                        "noodle_form": user_form,
                        "formset": formset,
                        })
            else:
 
                return render(request, 'my_profile.html', {
                    "noodle": pk,
                    "noodle_form": user_form,
                    "formset": formset,
                    })
        else:
 
            return render(request, 'my_profile.html', {
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

def uploads(request):
    # Have to add for profile not existing
    pk = request.user.pk
    user = User.objects.get(pk=pk)
    profile = Profile.objects.get(user=user)
    room = RentingUser.objects.filter(user_profile=profile)
    rooms = room.filter(deleted=False)
    pg = RentingPGUser.objects.filter(user_profile=profile)
    pgs = pg.filter(deleted=False)

    return render(request, 'my_upload.html',{'rooms':rooms,'pgs':pgs})

def delete_room(request, room_id):
    #Note: This works, but will always pass the result irrespective of the fact that the objects exsist or not.-Devansh Bhardwaj
    pk = request.user.pk
    user = User.objects.get(pk=pk)
    profile = Profile.objects.get(user=user)
    rooms = RentingUser.objects.filter(user_profile=profile)
    room  = rooms.filter(pk=room_id).first()
    room.deleted = True
    room.deleted_at = datetime.datetime.now()

    room.save()

    return redirect(uploads)

def delete_pg(request, pg_id):
    #Note: This works, but will always pass the result irrespective of the fact that the objects exsist or not.-Devansh Bhardwaj
    pk = request.user.pk
    user = User.objects.get(pk=pk)
    profile = Profile.objects.get(user=user)
    rooms = RentingPGUser.objects.filter(user_profile=profile)
    room  = rooms.filter(pk=pg_id).first()
    room.deleted = True
    room.deleted_at = datetime.datetime.now()

    room.save()

    return redirect(uploads)



def hide_pg(request, pg_id):
    #Will be used to hide the room
    pk = request.user.pk
    user = User.objects.get(pk=pk)
    profile = Profile.objects.get(user=user)
    rooms = RentingPGUser.objects.filter(user_profile=profile)
    room  = rooms.filter(pk=pg_id).first()
    #Till here we check that only the rooms uploaded by user can be hidden
    
    if (room.hidden == True):
        room.hidden = False
    else :
        room.hidden = True
        room.hidden_at = datetime.datetime.now()
    
    room.save()
  
    
    return redirect(uploads)

def hide_room(request, room_id):
    #Will be used to hide the room
    pk = request.user.pk
    user = User.objects.get(pk=pk)
    profile = Profile.objects.get(user=user)
    rooms = RentingUser.objects.filter(user_profile=profile)
    room  = rooms.filter(pk=room_id).first()
    #Till here we check that only the rooms uploaded by user can be hidden
    if (room.hidden == True):
        room.hidden = False
    else :
        room.hidden = True
        room.hidden_at = datetime.datetime.now()
    room.save()
    return redirect(uploads)

def room_update(request, room_id):
    pk = request.user.pk
    user = User.objects.get(pk=pk)
    profile = Profile.objects.get(user=user)
    rooms = RentingUser.objects.filter(user_profile=profile,pk=room_id).first()
    ImageFormSet = modelformset_factory(Images, form=ImageForm, extra=5, max_num=5,can_delete=True)
    user_form = RentForm(instance=rooms)
    
    if request.user.is_authenticated and request.user.id == user.id:
        rooms = RentingUser.objects.filter(user_profile=profile,pk=room_id).first()
        imageid = Images.objects.filter(user=room_id)
        if request.method =='POST':
            imageid = Images.objects.filter(user=room_id)
            form = RentForm(request.POST, instance=rooms)
            imageform = ImageFormSet(request.POST, request.FILES)
            if form.is_valid() and imageform.is_valid():
                form.save()
                for index, pic in enumerate(imageform):
                
                    if pic.cleaned_data:
                        
                        if pic.cleaned_data['id'] is None:
                            image = pic.cleaned_data['image']
                            
                            photo = Images(user=rooms, image=image)
                        
                            photo.save()
                        elif pic.cleaned_data['image'] is False:
                            photo = Images.objects.get(id=request.POST.get('form-' + str(index) + '-id'))
                            photo.delete()

                        else:
                            image = pic.cleaned_data.get('image')
                            photo = Images(user=rooms, image=image)
                            d = Images.objects.get(id=imageid[index].id)
                            d.image = photo.image
                            d.save()
                imageid = imageid.first()
                return render(request, 'room_detail.html', {
                    "prof": profile,
                    "rooms": rooms,
                    "images": imageid,
                    })
            else :
                print(form.error and imageform.errors)
        else :
            imageform = ImageFormSet(queryset=Images.objects.filter(user=room_id))   
            return render(request, 'upload_edit.html', {
                    "noodle": pk,
                    "form": user_form,
                    "imageform": imageform,
                    'header':'Room Update'})
    else:
        raise PermissionDenied

def pg_update(request, pg_id):
    pk = request.user.pk
    user = User.objects.get(pk=pk)
    profile = Profile.objects.get(user=user)
    rooms = RentingPGUser.objects.filter(user_profile=profile,pk=pg_id).first()
    ImageFormSet = modelformset_factory(ImagesPG, form=ImageFormPG, extra=5, max_num=5,can_delete=True)
    user_form = RentPGForm(instance=rooms)
    
    if request.user.is_authenticated and request.user.id == user.id:
        rooms = RentingPGUser.objects.filter(user_profile=profile,pk=pg_id).first()
        imageid = ImagesPG.objects.filter(user=pg_id)
        if request.method =='POST':
            imageid = ImagesPG.objects.filter(user=pg_id)
            form = RentPGForm(request.POST, instance=rooms)
            imageform = ImageFormSet(request.POST, request.FILES)
            if form.is_valid() and imageform.is_valid():
                form.save()
                for index, pic in enumerate(imageform):
                
                    if pic.cleaned_data:
                        
                        if pic.cleaned_data['id'] is None:
                            image = pic.cleaned_data['image']
                            
                            photo = ImagesPG(user=rooms, image=image)
                        
                            photo.save()
                        elif pic.cleaned_data['image'] is False:
                            photo = ImagesPG.objects.get(id=request.POST.get('form-' + str(index) + '-id'))
                            photo.delete()

                        else:
                            image = pic.cleaned_data.get('image')
                            photo = ImagesPG(user=rooms, image=image)
                            d = ImagesPG.objects.get(id=imageid[index].id)
                            d.image = photo.image
                            d.save()
                imageid = imageid.first()
                return render(request, 'pg_detail.html', {
                    "prof": profile,
                    "rooms": rooms,
                    "images": imageid,
                    })
            else :
                print(form.error and imageform.errors)
        else :
            imageform = ImageFormSet(queryset=ImagesPG.objects.filter(user=pg_id))   
            return render(request, 'upload_edit.html', {
                    "noodle": pk,
                    "form": user_form,
                    "imageform": imageform,
                    'header':'Room Update'})
    else:
        raise PermissionDenied

def pg_view(request, room_id, image_id):
    rooms = RentingPGUser.objects.get(pk=room_id)
    images = ImagesPG.objects.get(pk=image_id)
    seller = rooms.user_profile
    hide = 1
    try:
        pk = request.user.pk
        user = User.objects.get(pk=pk)
        profile = Profile.objects.get(user=user)
        return render(request, 'pg_detail.html', {'rooms': rooms, 'images': images, 'hide': hide, 'prof': profile, "pg":'kyahaiyeh'})
    
    except ObjectDoesNotExist:
        return render(request, 'pg_detail.html', {'rooms': rooms, 'images': images, 'seller': seller})

def room_view(request, room_id, image_id):
    rooms = RentingUser.objects.get(pk=room_id)
    images = Images.objects.get(pk=image_id)
    seller = rooms.user_profile
    hide = 1
    try:
        pk = request.user.pk
        user = User.objects.get(pk=pk)
        profile = Profile.objects.get(user=user)
        return render(request, 'room_detail.html', {'rooms': rooms, 'images': images, 'hide': hide, 'prof': profile, "body":"room"})

    except ObjectDoesNotExist:
        return render(request, 'room_detail.html', {'rooms': rooms, 'images': images, 'seller': seller})



