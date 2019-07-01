from django.db import models
from accounts.models import Profile
from django.contrib.auth.models import User
from django.db.models.signals import post_save

y_n_choices = [
    ('yes', 'Yes'),
    ('no', 'No'),
]


class RentingUser(models.Model):
    user_profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    number_of_rooms = models.IntegerField()
    price = models.CharField(max_length=50, default='')
    locality = models.CharField(max_length=100, default='')
    contact_number = models.CharField(max_length=10, default='')
    maximum_no_of_occupants = models.IntegerField()
    attached_bathroom = models.CharField(max_length=3, choices=y_n_choices, default='')
    attached_kitchen = models.CharField(max_length=15, choices=y_n_choices, default='')
    drive_in = models.CharField(max_length=3, choices=y_n_choices, default='')
    parking = models.CharField(max_length=3, choices=y_n_choices, default='')
    water_bill_included = models.CharField(max_length=3, choices=y_n_choices, default='')
    electricity_bill_included = models.CharField(max_length=3, choices=y_n_choices, default='')
    preferred_customer = models.CharField(max_length=50, choices=[('Family Preferred', 'Family Preferred'),
                                                                  ('Student Preferred', 'Student Preferred'),
                                    ('No Such Preference for Customer', 'No Such Preference for Customer')], default='')
    gender_preference = models.CharField(max_length=50, choices=[('Female Preferred', 'Females Preferred'),
                                                                 ('Males Preferred', 'Males Preferred'),
                                                        ('No Gender Preference', 'No Gender Preference')], default='')
    alternate_contact_number = models.CharField(max_length=10, default="", blank=True)
    preferred_contact_time = models.CharField(max_length=50, default='')
    any_other = models.TextField(max_length=100, default="", blank=True)
    
    #Adding for security adn better functionality
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    approved = models.BooleanField(default=False)

    def __str__(self):
        return str(self.user_profile)

class RentingPGUser(models.Model):
    user_profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    occupants_per_room = models.IntegerField()
    price = models.CharField(max_length=50, default='')
    locality = models.CharField(max_length=100, default='')
    attached_bathroom = models.CharField(max_length=3, choices=y_n_choices, default='')
    food_included = models.CharField(max_length=15, choices=y_n_choices, default='')
    drive_in = models.CharField(max_length=3, choices=y_n_choices, default='')
    parking = models.CharField(max_length=3, choices=y_n_choices, default='')
    water_bill_included = models.CharField(max_length=3, choices=y_n_choices, default='')
    electricity_bill_included = models.CharField(max_length=3, choices=y_n_choices, default='')
    preferred_customer = models.CharField(max_length=50, choices=[('Family Preferred', 'Family Preferred'),
                                                                  ('Student Preferred', 'Student Preferred'),
                                        ('No Preference For Customer', 'No Preference for Customer')], default='')
    gender_preference = models.CharField(max_length=50, choices=[('Female Preferred', 'Females Preferred'),
                                                                 ('Males Preferred', 'Males Preferred'),
                                                        ('No Gender Preference', 'No Gender Preference')], default='')
    preferred_contact_time = models.CharField(max_length=50, default='')
    contact_number = models.CharField(max_length=10, default='')
    alternate_contact_number = models.CharField(max_length=10, default='', blank=True)
    any_other = models.TextField(max_length=100, blank=True, default='')
    timings = models.CharField(max_length=50, blank=True, default='')

    #Adding for security adn better functionality
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    approved = models.BooleanField(default=False)

    def __str__(self):
        return str(self.user_profile)






def user_directory_path(instance, filename):

    return 'Images/user_{0}/{1}'.format(instance.user.id, filename)


def user_directory_path_pg(instance, filename):

    return 'ImagesPG/user_{0}/{1}'.format(instance.user.id, filename)


class Images(models.Model):
    user = models.ForeignKey(RentingUser, default=None, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=user_directory_path, verbose_name='Image')

    def __str__(self):
        return str(self.image)


class ImagesPG(models.Model):
    user = models.ForeignKey(RentingPGUser, default=None, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=user_directory_path_pg, verbose_name='ImagePG')

    def __str__(self):
        return str(self.image)
