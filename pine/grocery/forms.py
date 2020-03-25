from django import forms 
from django.contrib.auth.models import User
from .models import Product, Shop, Images
from main.models import Location
# (Use this link to https://stackoverflow.com/questions/5119994/get-current-user-in-django-form)
class ProductForm(forms.ModelForm): 
    
    class Meta:
        model = Product
        exclude = ['off', 'shop','free']
        widgets = {
            'name' : forms.TextInput(attrs = {'class': 'form-control'}),
            'quantity' : forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter the Cost Per Month'}),
            'selling_price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter the Cost Per Month'}),
            'barcode': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter the Cost Per Month'}),            
            'description' : forms.TextInput(attrs = {'class': 'form-control'}),
            'brand' : forms.Select(attrs = {'class': 'regDropDown'}),
            'category' : forms.SelectMultiple(attrs = {'class': 'regDropDown'}),
            'free_product' : forms.Select(attrs = {'class': 'regDropDown'}),
        }
    def __init__(self, shop, *args, **kwargs):
        self.shop = shop
        super(ProductForm,self).__init__(*args, **kwargs)
        self.fields['free_product'].queryset = Product.objects.filter(shop=shop)

class ImageForm(forms.ModelForm):
    image = forms.ImageField(label='Product Image')

    class Meta:
        model = Images
        fields = ('image', )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].required = False

class DeliveryLocationForm(forms.Form):
    
    location = forms.ModelChoiceField(queryset=Location.objects.all())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['location'].queryset = Location.objects.all()
