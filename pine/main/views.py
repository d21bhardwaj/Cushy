from django.shortcuts import render, redirect
from django.contrib.auth import logout
from .forms import RentForm, ImageForm
from django.forms import modelformset_factory
from .models import Images
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
