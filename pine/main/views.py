from django.shortcuts import render, redirect
from django.contrib.auth import logout
from .forms import RentForm


def index(request):
    return render(request, 'index.html')


def logout_view(request):
    logout(request)
    return redirect('index')


def rentdetails(request):
    if request.method == "POST":
        form = RentForm(request.POST)
        if form.is_valid():
            form.save()

    form = RentForm()
    return render(request, 'form.html', {'form': form})
