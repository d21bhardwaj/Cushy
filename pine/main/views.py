from django.shortcuts import render, redirect
from django.contrib.auth import logout
from .forms import RentForm, RentPGForm, ImageForm, ContactForm, ImageFormPG, FilterFormLocation, FilterFormPrice, FilterFormPGPrice
from django.forms import modelformset_factory
from .models import Images, ImagesPG, RentingUser, RentingPGUser, Location
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

def user_verified(user):
    try:
        return user.profile.is_verified()
    except ObjectDoesNotExist:
        return False 
       
def about_us(request):
    return render(request, 'about_us.html')

def index(request):
    return render(request, 'home.html')

def privacy(request):
   
    return FileResponse( open('static/privacy-policy.pdf', 'rb'), content_type='application/pdf')

def sitemap(request):
    return render(request,'sitemap.html')

def logout_view(request):
    logout(request)
    return redirect('index')

def about_us(request):
    return render(request, 'about_us.html')


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


                template = get_template('alert_room.txt')
                context = {
                        'value':'room'
                    }
                content = template.render(context)
        
                email = EmailMessage(
                    "New Room submission",
                    content,
                    "CushyRooms Room Approval" +'',
                    ['project.pinetown@gmail.com'],
                    headers = {'Reply-To': 'project.pinetown@gmail.com' }
                )
                email.send()

                return render(request,"message.html",{"background":"bg-success","title":"Successfully Submitted","head":"Successfully Submitted","body":"Your Room Will be Shown after viewing details submitted by you. Please wait till then!"})
            else:
                print(form.errors, imageform.errors)
        else:
            form = RentForm()
            imageform = ImageFormSet(queryset=Images.objects.none())
        return render(request, 'form.html', {'form': form, 'imageform': imageform , 'header':'Room Details'})
    else:
        raise PermissionDenied      

@login_required
@user_passes_test(user_verified, login_url='/settings/account/')
def rentpgdetails(request):
    pk = request.user.pk
    user = User.objects.get(pk=pk)
    profile = Profile.objects.get(user=user)

    ImageFormSet = modelformset_factory(ImagesPG, form=ImageFormPG, extra=5)
    if request.user.is_authenticated and request.user.id == user.id:

        if request.method == "POST":
            form = RentPGForm(request.POST)
            imageform = ImageFormSet(request.POST, request.FILES, queryset=ImagesPG.objects.none())
            if form.is_valid() and imageform.is_valid():
                post_form = form.save(commit=False)
                post_form.user_profile = profile
                post_form.save()
                
                for pic in imageform.cleaned_data:
                    print(pic)
                    if pic:
                        image = pic['image']
                        print(image, "Image")
                        print(pic, "pic")
                        photo = ImagesPG(user=profile, room_pg=post_form, image=image)
                       # print(image.cleaned_data)
                        
                        photo.save()
                        print(photo)
                print(ImagesPg)
                
                template = get_template('alert_room.txt')
                context = {
                        'value':'pg'
                    }
                content = template.render(context)
        
                email = EmailMessage(
                    "New Room submission",
                    content,
                    "CushyRooms Room Approval" +'',
                    ['project.pinetown@gmail.com'],
                    headers = {'Reply-To': 'project.pinetown@gmail.com' }
                )
                email.send()
                return render(request,"message.html",{"background":"bg-success","title":"Successfully Submitted","head":"Successfully Submitted","body":"Your PG Will be Shown after viewing details submitted by you. Please wait till then!"})
            else:
                print(form.errors, imageform.errors)
        else:
            form = RentPGForm()
            imageform = ImageFormSet(queryset=ImagesPG.objects.none())
        return render(request, 'form.html', {'form': form, 'imageform': imageform , 'header':'Pg Details'})
    else:
        raise PermissionDenied      


def renttype(request):
    return render(request, 'choice.html' ,{'header': 'Choose Type of Renting'})


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
            contact_number = request.POST.get(
                'contact_number'
            , '')
            form_content = request.POST.get('content', '')

            # Email the profile with the
            # contact information
            template = get_template('contact_template.txt')
            context = {
                'contact_name': contact_name,
                'contact_email': contact_email,
                'contact_number': contact_number,
                'form_content': form_content,
            }
            content = template.render(context)
    
            email = EmailMessage(
                "New contact form submission",
                content,
                "CushyRooms Contact Form" +'',
                ['project.pinetown@gmail.com'],
                headers = {'Reply-To': contact_email }
            )
            email.send()
            return render(request,"message.html",{"background":"bg-success","title":"Successfully Submitted","head":"Successfully Submitted","body":"We are grateful you contacted us ,  will revert back to you soon."})

    return render(request, 'contact_us.html', {
        'form': form_class,'header':'Contact Us'
    })

#To view all the rooms

def allrooms(request):
    rooms = RentingUser.objects.filter(approved=True, deleted=False, hidden=False)
    location = Location.objects.all()
    if request.method == 'POST':
        form1 = FilterFormLocation(data=request.POST)
        form2 = FilterFormPrice(data=request.POST)
        if form1.is_valid() or form2.is_valid():
            room_filter = rooms
            if(form1.is_valid()):
                locations = form1.cleaned_data.get('Locations')
                room_filter = rooms.filter(locality__in = locations)
            if(form2.is_valid()):
                prices = form2.cleaned_data.get('Prices')
            
                temp = -1
                temp2 = 0
                for p in prices:
                    if(temp==-1):
                        temp = p
                    if(temp2<=int(p)):
                        temp2 = (int(p)+2000)
                room_filter = room_filter.filter(price__range=(temp,temp2))
            
            return render(request, 'filter_room.html', {
                'form1': form1,'form2':form2, 'rooms': room_filter
            })
        else:
            form1 = FilterFormLocation()
            form2 = FilterFormPrice()
        
    else:
        form1 = FilterFormLocation()
        form2 = FilterFormPrice()
        
    
    return render(request, 'all_rooms.html', {'form1':form1,'form2' : form2, 'rooms': rooms, 'location' : location})

#To view all the PGs

def allpgs(request):
    rooms = RentingPGUser.objects.filter(approved=True, deleted=False, hidden=False)
    location = Location.objects.all()
    print(location)
    if request.method == 'POST':
        form1 = FilterFormLocation(data=request.POST)
        form2 = FilterFormPGPrice(data=request.POST)
        if form1.is_valid() or form2.is_valid():
            room_filter = rooms
            if(form1.is_valid()):
                locations = form1.cleaned_data.get('Locations')
                room_filter = rooms.filter(locality__in = locations)
            if(form2.is_valid()):
                prices = form2.cleaned_data.get('Prices')
            
                temp = -1
                temp2 = 0
                for p in prices:
                    if(temp==-1):
                        temp = p
                    if(temp2<=int(p)):
                        temp2 = (int(p)+2000)
                room_filter = room_filter.filter(price__range=(temp,temp2))
            
            return render(request, 'filter_pg.html', {
                'form1': form1,'form2':form2, 'rooms': room_filter
            })
        else:
            form1 = FilterFormLocation()
            form2 = FilterFormPGPrice()
        
    else:
        form1 = FilterFormLocation()
        form2 = FilterFormPGPrice()

    return render(request, 'all_pgs.html', {'form1':form1,'form2' : form2, 'rooms': rooms, 'location' : location})

#Detail of the room selected

def detailroom(request, room_id, image_id):
    rooms = RentingUser.objects.get(pk=room_id)
    images = Images.objects.get(pk=image_id)
    seller = rooms.user_profile
    try:
        pk = request.user.pk
        user = User.objects.get(pk=pk)
        profile = Profile.objects.get(user=user)
        return render(request, 'room_detail.html', {'rooms': rooms, 'images': images, 'seller': seller, 'prof': profile})
    except ObjectDoesNotExist:
        return render(request, 'room_detail.html', {'rooms': rooms, 'images': images, 'seller': seller})
       

def detailpg(request, room_id, image_id):
    rooms = RentingPGUser.objects.get(pk=room_id)
    images = ImagesPG.objects.get(pk=image_id)
    seller = rooms.user_profile
    try:
        pk = request.user.pk
        user = User.objects.get(pk=pk)
        profile = Profile.objects.get(user=user)
        return render(request, 'pg_detail.html', {'rooms': rooms, 'images': images, 'seller': seller, 'prof': profile})
    
    except ObjectDoesNotExist:
        return render(request, 'pg_detail.html', {'rooms': rooms, 'images': images, 'seller': seller})
       
