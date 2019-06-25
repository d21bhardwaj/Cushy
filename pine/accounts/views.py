from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login
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

@login_required
def profileupdate(request):
    pk = request.user.pk
    user = User.objects.get(pk=pk)
    user_form = ProfileForm(instance=user)
 
    ProfileInlineFormset = inlineformset_factory( User, model=Profile, fields=('name','mobile_no','email'))
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
                    return redirect('index')
        else:
 
            return render(request, 'my_account.html', {
                "noodle": pk,
                "noodle_form": user_form,
                "formset": formset,
                })
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
    return render(request, 'my_account.html', {'form': form})