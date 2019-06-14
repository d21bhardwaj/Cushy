from django.shortcuts import render, redirect
from django.contrib.auth import logout
from .forms import RentForm, ImageForm, ContactForm
from django.forms import modelformset_factory
from .models import Images
#adding for contact form
from django.core.mail import EmailMessage
from django.shortcuts import redirect
from django.template.loader import get_template



def index(request):
    return render(request, 'index.html')


def logout_view(request):
    logout(request)
    return redirect('index')


def rentdetails(request):
    ImageFormSet = modelformset_factory(Images, form=ImageForm, extra=6)
    if request.method == "POST":
        form = RentForm(request.POST)
        imageform = ImageFormSet(request.POST, request.FILES, queryset=Images.objects.none())

        if form.is_valid() and imageform.is_valid():
            form.save()
            imageform.save()

            return redirect('index')
        else:
            print(form.errors, imageform.errors)
    else:
        form = RentForm()
        imageform = ImageFormSet(queryset=Images.objects.none())
    return render(request, 'form.html', {'form': form, 'imageform': imageform})

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