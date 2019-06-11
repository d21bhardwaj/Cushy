from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login
#from django.contrib.auth.forms import UserCreationForm 
from .forms import SignUpForm

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
    return render(request, 'signup.html',{'form': form})