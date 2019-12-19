from django.db import models
from accounts.models import Profile
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.utils.timezone import now
from django.core.exceptions import ValidationError
y_n_choices = [
    ('yes', 'Yes'),
    ('no', 'No'),
]
s_i_choices = [
    ('sh', 'Shared'),
    ('in', 'Individual'),
]

class Location(models.Model):
    location = models.CharField(max_length=30, null = True, default='')

    def __str__(self):
        return str(self.location)

class RentingUser(models.Model):
    user_profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=False)
    number_of_rooms = models.IntegerField()
    price = models.CharField(max_length=50, default='')
    locality = models.ForeignKey(Location, on_delete=models.DO_NOTHING,  primary_key=False, null=True,default='')
    maximum_no_of_occupants = models.IntegerField()
    attached_bathroom = models.CharField(max_length=3, choices=s_i_choices, default='no')
    attached_kitchen = models.CharField(max_length=15, choices=y_n_choices, default='no')
    drive_in = models.CharField(max_length=3, choices=y_n_choices, default='no')
    parking = models.CharField(max_length=3, choices=y_n_choices, default='no')
    water_bill_included = models.CharField(max_length=3, choices=y_n_choices, default='no')
    electricity_bill_included = models.CharField(max_length=3, choices=y_n_choices, default='no')
    preferred_customer = models.CharField(max_length=50, choices=[('Family Preferred', 'Family Preferred'),
                                                                ('Working Preferred', 'Working Preferred'),
                                                                ('Student Preferred', 'Student Preferred'),
                                                                ('no', 'No Such Preference')],
                                                                 default='no')
    gender_preference = models.CharField(max_length=50, choices=[('Only Girls', 'Only Girls'),
                                                                 ('Only Boys', 'Only Boys'),
                                                                ('no', 'No Gender Preference')],
                                                                 default='no')
    alternate_contact_number = models.CharField(max_length=10, default="", blank=True)
    preferred_contact_time = models.CharField(max_length=50, default='')
    any_other = models.TextField(max_length=100, default="", blank=True)
    
    #Adding for security and better functionality
    created_at = models.DateTimeField(default=now, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)
    approved = models.BooleanField(default=False)

    #Adding if a user wants to hide the room uploaded
    hidden = models.BooleanField(default=False)
    hidden_at = models.DateTimeField(null= True, blank=True)

    deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null= True, blank=True)

    def __str__(self):
        return str(self.id)

class RentingPGUser(models.Model):
    user_profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    occupants_per_room = models.IntegerField()
    price = models.CharField(max_length=50, default='')
    locality = models.ForeignKey(Location, on_delete=models.DO_NOTHING,  primary_key=False, null=True,default='')
    attached_bathroom = models.CharField(max_length=3, choices=y_n_choices, default='no')
    food_included = models.CharField(max_length=15, choices=y_n_choices, default='no')
    drive_in = models.CharField(max_length=3, choices=y_n_choices, default='no')
    parking = models.CharField(max_length=3, choices=y_n_choices, default='no')
    water_bill_included = models.CharField(max_length=3, choices=y_n_choices, default='no')
    electricity_bill_included = models.CharField(max_length=3, choices=y_n_choices, default='no')
    preferred_customer = models.CharField(max_length=50, choices=[('Working Preferred', 'Working Preferred'),
                                                                  ('Student Preferred', 'Student Preferred'),
                                        ('no ', 'No Preference ')], default='no')
    gender_preference = models.CharField(max_length=50, choices=[('Only Girls', 'Only Girls'),
                                                                 ('Only Boys', 'Only Boys'),
                                                        ], default='')
    preferred_contact_time = models.CharField(max_length=50, default='')

    alternate_contact_number = models.CharField(max_length=10, default='', blank=True)
    any_other = models.TextField(max_length=100, blank=True, default='')
    timings = models.CharField(max_length=50, blank=True, default='')

    #Adding for security adn better functionality
    created_at = models.DateTimeField(default=now, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)
    approved = models.BooleanField(default=False)

     #Adding if a user wants to hide the room uploaded
    hidden = models.BooleanField(default=False)
    hidden_at = models.DateTimeField(null= True, blank=True)

    deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null= True, blank=True)

    def __str__(self):
        return str(self.id)



def validate_image(fieldfile_obj):
    filesize = fieldfile_obj.file.size
    megabyte_limit = 2.0
    if filesize > megabyte_limit*1024*1024:
        raise ValidationError('File size must be under 2MB. Current file size is %.2fMB.' %  (filesize/1024/1024))


def user_directory_path(instance, filename):
    prof = instance.user.user_profile
    no = instance.user 
    return 'Images/user_{id}/room_{no}/{file}'.format(id=prof.id,no= no , file = filename)
    #return 'Images/user_{0}/{1}'.format(instance.user.id, filename)


def user_directory_path_pg(instance, filename):
    prof = instance.user.user_profile
    no = instance.user 
    return 'ImagesPg/user_{id}/room_{no}/{file}'.format(id=prof.id,no= no , file = filename)
   


class Images(models.Model):
    user = models.ForeignKey(RentingUser, default=None, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=user_directory_path, validators=[validate_image],verbose_name='Image')

    def __str__(self):
        return str(self.image)


class ImagesPG(models.Model):
    # user = models.ForeignKey(RentingUser, default=None, on_delete=models.CASCADE)
    user = models.ForeignKey(RentingPGUser, default=None, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=user_directory_path_pg,validators=[validate_image], verbose_name='ImagePG')

    def __str__(self):
        return str(self.image)
