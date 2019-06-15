from django.db import models


y_n_choices = [
    ('yes', 'Yes'),
    ('no', 'No'),
]


class RentingUser(models.Model):
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
    preferred_customer = models.CharField(max_length=50, choices=[('family', 'Family'), ('student', 'Student'),
                                ('others (Specify)', 'Others (Specify)'), ('no such preference', 'No Such Preference')], default='')
    gender_preference = models.CharField(max_length=10, choices=[('only female', 'Only Female'),
                                                                 ('only male', 'Only Male'), ('none', 'None')], default='')
    alternate_contact_number = models.CharField(max_length=10, default="", blank=True)
    preferred_contact_time = models.CharField(max_length=50, default='')
    any_other = models.TextField(max_length=100, default="", blank=True)

    def __str__(self):
        return self.contact_number


class RentingPGUser(models.Model):
    occupants_per_room = models.IntegerField()
    price = models.CharField(max_length=50, default='')
    locality = models.CharField(max_length=100, default='')
    attached_bathroom = models.CharField(max_length=3, choices=y_n_choices, default='')
    attached_kitchen = models.CharField(max_length=15, choices=y_n_choices, default='')
    drive_in = models.CharField(max_length=3, choices=y_n_choices, default='')
    parking = models.CharField(max_length=3, choices=y_n_choices, default='')
    water_bill_included = models.CharField(max_length=3, choices=y_n_choices, default='')
    electricity_bill_included = models.CharField(max_length=3, choices=y_n_choices, default='')
    preferred_customer = models.CharField(max_length=50, choices=[('family', 'Family'), ('student', 'Student'),
                                                                  ('others (Specify)', 'Others (Specify)'),
                                                                  ('no such preference', 'No Such Preference')], default='')
    gender_preference = models.CharField(max_length=10, choices=[('only female', 'Only Female'),
                                                                 ('only male', 'Only Male'), ('none', 'None')], default='')
    preferred_contact_time = models.CharField(max_length=50, default='')
    contact_number = models.CharField(max_length=10, default='')
    alternate_contact_number = models.CharField(max_length=10, default='')
    any_other = models.TextField(max_length=100, blank=True, default='')
    timings = models.CharField(max_length=50, blank=True, default='')

    def __str__(self):
        return self.contact_number


def user_directory_path(instance, filename):

    return 'Images/user_{0}/{1}'.format(instance.user.id, filename)


def user_directory_path_PG(instance, filename):

    return 'ImagesPG/user_{0}/{1}'.format(instance.user.id, filename)


class Images(models.Model):
    user = models.ForeignKey(RentingUser, default=None, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=user_directory_path, verbose_name='Image')

    def __str__(self):
        return str(self.image)


class ImagesPG(models.Model):
    user = models.ForeignKey(RentingPGUser, default=None, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=user_directory_path_PG, verbose_name='ImagePG')

    def __str__(self):
        return str(self.image)