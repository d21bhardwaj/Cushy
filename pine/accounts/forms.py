from django import forms 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile 
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column

class SignUpForm(UserCreationForm):
    email = forms.CharField(max_length=254, required=True, widget=forms.EmailInput())
    
    class Meta:
        model = User
        fields = ('username','first_name','last_name', 'email', 'password1','password2')

#Custom user profile made
class ProfileForm(forms.ModelForm):
    
    class Meta:
        model = Profile
        fields = ['id', 'title', 'name','mobile_no','email','verified']
         
       
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Column('title', css_class='form-group col-md-2 mb-0'),
                Column('name', css_class='form-group col-md-6 mb-0'),
                
                css_class='form-row'
            ),
            Row(
                Column('mobile_no', css_class='form-group col-md-6 mb-0'),
                
                
                css_class='form-row'
            ),
             Row(
               
                Column('email', css_class='form-group col-md-6 mb-0'),
                
                css_class='form-row'
            )
        )

class LocationForm(forms.ModelForm):
    
    class Meta:
        model = Profile
        fields = ('location',)