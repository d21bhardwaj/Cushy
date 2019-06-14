from django import forms
from .models import RentingUser, Images


class RentForm(forms.ModelForm):

    class Meta:
        model = RentingUser
        fields = ('name', 'contact_number', 'number_of_rooms', 'locality', 'parking', 'balcony', 'individual',
                  'attached_bathroom', 'kitchen', 'contact_time', 'prefered_customer', 'gender_pref', 'Paying_guest', 'people_per_room',
                  'food',)
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Your Full Name'}),
            'contact_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Contact Number'}),
            'number_of_rooms': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter the Number of Rooms in the House'}),
            'locality': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Locality'}),
            'parking': forms.Select(attrs={'class':'regDropDown'}),
            'balcony': forms.Select(attrs={'class':'regDropDown'}),
            'individual': forms.Select(attrs={'class':'regDropDown'}),
            'attached_bathroom': forms.Select(attrs={'class':'regDropDown'}),
            'kitchen': forms.Select(attrs={'class':'regDropDown'}),
            'contact_time': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Preferred Contact Time'}),
            'prefered_customer': forms.Select(attrs={'class':'regDropDown'}),
            'gender_pref': forms.Select(attrs={'class':'regDropDown'}),
            'Paying_guest': forms.CheckboxInput(attrs={'class': 'form-control'}),
            'people_per_room': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'how many Tenants per room (if PG)'}),
            'food': forms.Select(attrs={'class':'regDropDown'}),
        }

class ImageForm(forms.ModelForm):
    image = forms.ImageField(label='Image')
    class Meta:
        model = Images
        fields = ('image', )