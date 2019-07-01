from django.shortcuts import render, redirect
from django.contrib.auth import logout
from .forms import RentForm, RentPGForm, ImageForm, ContactForm, ImageFormPG
from django.forms import modelformset_factory
from .models import Images, ImagesPG, RentingUser, RentingPGUser
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


def user_verified(user):
    if user.profile:
        return user.profile.is_verified()
    else:
        return False


def index(request):
    return render(request, 'index.html')


def logout_view(request):
    logout(request)
    return redirect('index')


@login_required
@user_passes_test(user_verified, login_url='/settings/account/')
def rentdetails(request):
    pk = request.user.pk
    user = User.objects.get(pk=pk)
    profile = Profile.objects.get(user=user)
   
  
    ImageFormSet = modelformset_factory(Images, form=ImageForm, extra=3)
    if request.user.is_authenticated and request.user.id == user.id:
        if request.method == "POST":
            form = RentForm(request.POST,request.FILES, )
            imageform = ImageFormSet(request.POST, request.FILES, queryset=ImagesPG.objects.none())

            if form.is_valid() and imageform.is_valid():
                post_form = form.save(commit=False)
                post_form.user_profile = profile
                post_form.save()
                for pic in imageform.cleaned_data:
                    if pic:
                        image = pic['image']
                        photo = Images(user=post_form, image=image)
                        photo.save()
                return redirect('index')
            else:
                print(form.errors, imageform.errors)
        else:
            form = RentForm()
            imageform = ImageFormSet(queryset=Images.objects.none())
        return render(request, 'form.html', {'form': form, 'imageform': imageform})
    else:
        raise PermissionDenied      

@login_required
@user_passes_test(user_verified, login_url='/settings/account/')
def rentpgdetails(request):
    pk = request.user.pk
    user = User.objects.get(pk=pk)
    profile = Profile.objects.get(user=user)

    ImageFormSet = modelformset_factory(ImagesPG, form=ImageFormPG, extra=3)
    if request.user.is_authenticated and request.user.id == user.id:

        if request.method == "POST":
            form = RentPGForm(request.POST)
            imageform = ImageFormSet(request.POST, request.FILES, queryset=ImagesPG.objects.none())
            if form.is_valid() and imageform.is_valid():
                post_form = form.save(commit=False)
                post_form.user = request.user
                post_form.save()
                for pic in imageform.cleaned_data:
                    if pic:
                        image = pic['image']
                        photo = ImagesPG(user=post_form, image=image)
                        photo.save()
                return redirect('index')
            else:
                print(form.errors, imageform.errors)
        else:
            form = RentPGForm()
            imageform = ImageFormSet(queryset=ImagesPG.objects.none())
        return render(request, 'form.html', {'form': form, 'imageform': imageform})
    else:
        raise PermissionDenied      



def renttype(request):
    return render(request, 'choice.html')


#For contact form
# our view


def contact(request):
    form_class = ContactForm

    # new logic!
    if request.method == 'POST':
        form = form_class(data=request.POST)

        if form.is_valid():
            contact_name = request.POST.get(
                'contact_name'
            , '')
            contact_email = request.POST.get(
                'contact_email'
            , '')
            form_content = request.POST.get('content', '')

            # Email the profile with the
            # contact information
            template = get_template('contact_template.txt')
            context = {
                'contact_name': contact_name,
                'contact_email': contact_email,
                'form_content': form_content,
            }
            content = template.render(context)

            email = EmailMessage(
                "New contact form submission",
                content,
                "Your website" +'',
                ['youremail@gmail.com'],
                headers = {'Reply-To': contact_email }
            )
            email.send()
            return redirect('contact_us')

    return render(request, 'contact_us.html', {
        'form': form_class,
    })

#To view all the rooms
def allrooms(request):
    rooms = RentingUser.objects.all()
    
    return render(request, 'all_rooms.html', {'rooms': rooms})

#To view all the PGs

def allpgs(request):
    rooms = RentingPGUser.objects.all()
    return render(request, 'all_pgs.html', {'rooms': rooms})

#Detail of the room selected
@login_required()
def detailroom(request, room_id, image_id):
    rooms = RentingUser.objects.get(pk=room_id)
    images = Images.objects.get(pk=image_id)
    seller = rooms.user_profile
    return render(request, 'room_detail.html', {'rooms': rooms, 'images': images, 'seller': seller})

@login_required()
def detailpg(request, room_id, image_id):
    rooms = RentingPGUser.objects.get(pk=room_id)
    images = ImagesPG.objects.get(pk=image_id)
    seller = rooms.user_profile
    return render(request, 'pg_detail.html', {'rooms': rooms, 'images': images, 'seller': seller})

