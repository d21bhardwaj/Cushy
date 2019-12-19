from django import forms
from .models import RentingUser, RentingPGUser, Images, ImagesPG, Location
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, ButtonHolder
from django.template.defaultfilters import filesizeformat

class RentForm(forms.ModelForm):

    class Meta:
        model = RentingUser
        labels = {
            'gender_preference': 'Only Boys/Girls',
            'attached_bathroom': 'Bathroom '
        }
        fields = ('number_of_rooms', 'price', 'maximum_no_of_occupants', 'locality', 'attached_bathroom',
                  'attached_kitchen', 'drive_in', 'parking', 'water_bill_included', 'electricity_bill_included',
                  'preferred_customer', 'gender_preference', 'preferred_contact_time',
                  'alternate_contact_number', 'any_other')
        widgets = {
            'number_of_rooms': forms.NumberInput(attrs={'class': 'form-control',
                                                        'placeholder': 'Enter the Number of Rooms in the House'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter the Cost Per Month'}),
            'locality':  forms.Select(attrs={'class': 'regDropDown'}),
            'attached_bathroom': forms.Select(attrs={'class': 'regDropDown'}),
            'attached_kitchen': forms.Select(attrs={'class': 'regDropDown'}),
            'maximum_no_of_occupants': forms.NumberInput(attrs={'class': 'form-control',
                                                                'placeholder':
                                                                'Enter Maximum number of People that can stay there'}),
            'drive_in': forms.Select(attrs={'class': 'regDropDown'}),
            'parking': forms.Select(attrs={'class':'regDropDown'}),
            'water_bill_included': forms.Select(attrs={'class':'regDropDown'}),
            'electricity_bill_included': forms.Select(attrs={'class': 'regDropDown'}),
            'preferred_customer': forms.Select(attrs={'class': 'regDropDown'}),
            'gender_preference': forms.Select(attrs={'class': 'regDropDown'}),
            'preferred_contact_time': forms.TextInput(attrs={'class': 'form-control',
                                                             'placeholder': 'Your Preferred Contact Time Eg. 5-9 pm'}),
            'alternate_contact_number': forms.TextInput(attrs={'class': 'form-control',
                                                               'placeholder': 'Enter Contact Number'}),
            'any_other': forms.Textarea(attrs={'placeholder': "Any Other Specification Or Something you would wan't to clarify about your property!"})
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Column('number_of_rooms', css_class='form-group col-md-4 mb-0'),
                Column('locality', css_class='form-group col-md-4 mb-0'),
                
                css_class='form-row'
            ),
            Row(
                Column('price', css_class='form-group col-md-4 mb-0'),
                Column('maximum_no_of_occupants', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('attached_bathroom', css_class='form-group col-md-4 mb-0'),
                Column('attached_kitchen', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            Row(
                
                Column('drive_in', css_class='form-group col-md-4 mb-0'),
                Column('parking', css_class='form-group col-md-4 mb-0'),
               
                css_class='form-row'
            ),
             Row(
                
                
                Column('water_bill_included', css_class='form-group col-md-4 mb-0'),
                Column('electricity_bill_included', css_class='form-group col-md-4 mb-0'),
               
                css_class='form-row'
            ),
            Row(
                Column('preferred_customer', css_class='form-group col-md-4 mb-0'),
                Column('gender_preference', css_class='form-group col-md-4 mb-0'),
               
                css_class='form-row'
            ),
            Row(
                Column('preferred_contact_time', css_class='form-group col-md-4 mb-0'),
                Column('alternate_contact_number', css_class='form-group col-md-4 mb-0'),
                
                css_class='form-row'
            ),
            'any_other',
           
        
        )


class RentPGForm(forms.ModelForm):

    class Meta:
        model = RentingPGUser
        labels = {
            'gender_preference': 'Only Boys/Girls',
          
        }

        fields = ('occupants_per_room', 'price', 'locality', 'attached_bathroom', 'food_included', 'drive_in',
                  'parking', 'water_bill_included', 'electricity_bill_included', 'preferred_customer',
                  'gender_preference', 'preferred_contact_time', 'alternate_contact_number',
                  'any_other', 'timings')
        widgets = {
            'occupants_per_room': forms.NumberInput(attrs={'class': 'form-control',
                                                        'placeholder': 'Enter the Number of Rooms in the House'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter the Cost Per Month'}),
            'locality':  forms.Select(attrs={'class': 'regDropDown'}),  
            'attached_bathroom': forms.Select(attrs={'class': 'regDropDown'}),
            'food_included': forms.Select(attrs={'class': 'regDropDown'}),
            'drive_in': forms.Select(attrs={'class': 'regDropDown'}),
            'parking': forms.Select(attrs={'class': 'regDropDown'}),
            'water_bill_included': forms.Select(attrs={'class': 'regDropDown'}),
            'electricity_bill_included': forms.Select(attrs={'class': 'regDropDown'}),
            'preferred_customer': forms.Select(attrs={'class': 'regDropDown'}),
            'gender_preference': forms.Select(attrs={'class': 'regDropDown'}),
            'preferred_contact_time': forms.TextInput(attrs={'class': 'form-control',
                                                             'placeholder': 'Your Preferred Contact Time Eg. 5-9 pm'}),
            'alternate_contact_number': forms.TextInput(attrs={'class': 'form-control',
                                                               'placeholder': 'Enter Contact Number'}),
            'any_other': forms.Textarea(attrs={'placeholder': "Any Other Specification Or Something you would wan't to tell about your property!"}),
            'timings': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter In-Out Timings (if Any)'})

        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Column('gender_preference', css_class='form-group col-md-4 mb-0'),
                Column('locality', css_class='form-group col-md-4 mb-0'),
                
                css_class='form-row'
            ),
            Row(
                Column('price', css_class='form-group col-md-4 mb-0'),
                Column('occupants_per_room', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('attached_bathroom', css_class='form-group col-md-4 mb-0'),
                Column('food_included', css_class='form-group col-md-4 mb-0'),
                
                css_class='form-row'
            ),
            Row(
            
                Column('drive_in', css_class='form-group col-md-4 mb-0'),
                Column('parking', css_class='form-group col-md-4 mb-0'),
                
                css_class='form-row'
            ),
             Row(
                
               
                Column('water_bill_included', css_class='form-group col-md-4 mb-0'),
                Column('electricity_bill_included', css_class='form-group col-md-4 mb-0'),
               
                css_class='form-row'
            ),
            Row(
                Column('preferred_customer', css_class='form-group col-md-4 mb-0'),
    
                Column('preferred_contact_time', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('alternate_contact_number', css_class='form-group col-md-4 mb-0'),
                Column('timings', css_class='form-group col-md-4 mb-0'),  
                css_class='form-row'
            ),
            'any_other',
            
        
        )


class ImageForm(forms.ModelForm):
    image = forms.ImageField(label='Image')

    class Meta:
        model = Images
        fields = ('image', )
    # def clean(self):
    #     cleaned_data =super().clean()
    #     image = self.cleaned_data.get("image")
    #     if image.size > 2048*1024:
    #         raise forms.ValidationError(
    #             'File size must be under 2MB. Current file size is %.2fMB.' %  (image.size/1024/1024))
    #     return(image)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
class ImageFormPG(forms.ModelForm):
    image = forms.ImageField(label='ImagePG')

    class Meta:
        model = ImagesPG
        fields = ('image', )
    # def clean(self):
    #     cleaned_data =super().clean()
    #     image = self.cleaned_data.get("image")
    #     if image.size > 2048*1024:
    #         raise forms.ValidationError(
    #             'File size must be under 2MB. Current file size is %.2fMB.' %  (image.size/1024/1024))
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    


class FilterFormLocation(forms.ModelForm):
    LOCATION = ((x.id, x) for x in Location.objects.all())
    #print(LOCATION)
    Locations = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                                          choices=LOCATION)
    class Meta: 
        model = Location
        fields = ('Locations',)

class FilterFormPrice(forms.ModelForm):
    PRICE = (
        (0,'Less than 2000'),
        (2000,'2000-4000'),
        (4000,'4000-6000'),
        (6000,'6000-8000'),
        (8000,'8000-10000'),
        (10000,'Above 10000')
    )
    Prices = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                                          choices=PRICE)
    class Meta: 
        model = RentingUser 
        fields = ('Prices',)

                    

class FilterFormPGPrice(forms.ModelForm):
    PRICE = (
        (0,'Less than 2000'),
        (2000,'2000-4000'),
        (4000,'4000-6000'),
        (6000,'6000-8000'),
        (8000,'8000-10000'),
        (10000,'Above 10000')
    )
    Prices = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                                          choices=PRICE)
    class Meta: 
        model = RentingPGUser 
        fields = ('Prices',)     

class ContactForm(forms.Form):
    contact_name = forms.CharField(required=True)
    contact_email = forms.EmailField(required=True)
    contact_number = forms.IntegerField(required=True)
    content = forms.CharField(
        required=True,
        widget=forms.Textarea
    )
    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        self.fields['contact_name'].label = "Your name:"
        self.fields['contact_email'].label = "Your email:"
        self.fields['contact_number'].label = "Your mobile-number:"
        self.fields['content'].label ="Suggestions, Feedback, Want Something more!!"
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
        
            Row(
            Column('contact_name', css_class='form-group col-md-4 mb-0'),
           
            
            css_class='form-row centered'
            ),
            Row(
            Column('contact_email', css_class='form-group col-md-4 mb-0'),
           
            
            css_class='form-row centered'
            ),
            Row(
            Column('contact_number', css_class='form-group col-md-4 mb-0'),
           
            
            css_class='form-row centered'
            ),
            Row(
            Column('content', css_class='form-group col-md-4 mb-2'),
           
            
            css_class='form-row centered'
            ),
         
        )
