from django.shortcuts import render, redirect
from django.contrib.auth import logout
from .forms import RentForm, RentPGForm, ImageForm, ContactForm, ImageFormPG
from django.forms import modelformset_factory
from .models import Images, ImagesPG, RentingUser, RentingPGUser
#adding for contact form
from django.core.mail import EmailMessage
from django.shortcuts import redirect
from django.template.loader import get_template
from django.contrib.auth.decorators import login_required

def index(request):
    return render(request, 'index.html')


def logout_view(request):
    logout(request)
    return redirect('index')

@login_required
def rentdetails(request):
    ImageFormSet = modelformset_factory(Images, form=ImageForm, extra=3)
    if request.method == "POST":
        form = RentForm(request.POST)
        imageform = ImageFormSet(request.POST, request.FILES, queryset=ImagesPG.objects.none())

        if form.is_valid() and imageform.is_valid():
            post_form = form.save(commit=False)
            post_form.user = request.user
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

@login_required
def rentpgdetails(request):
    ImageFormSet = modelformset_factory(ImagesPG, form=ImageFormPG, extra=3)
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
    return render(request, 'room_detail.html', {'rooms': rooms, 'images': images})


