from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login
#from django.contrib.auth.forms import UserCreationForm Not needed now
from .forms import SignUpForm
# Now adding for Account View
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import UpdateView
from django.contrib.auth.forms import PasswordChangeForm, AdminPasswordChangeForm

from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from social_django.models import UserSocialAuth
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


#My account view

@method_decorator(login_required, name='dispatch')
class UserUpdateView(UpdateView):
    model = User
    fields =('first_name', 'last_name','email', )
    template_name = 'my_account.html'
    success_url = reverse_lazy('my_account')

    def get_object(self):
        return self.request.user



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
    return render(request, 'my_account.html', {'form': form})