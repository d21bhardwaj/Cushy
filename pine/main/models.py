from django.db import models


y_n_choices = [
    ('yes', 'Yes'),
    ('no', 'No'),
]


class RentingUser(models.Model):
    name = models.CharField(max_length=50)
    contact_number = models.CharField(max_length=10)
    number_of_rooms = models.IntegerField()
    locality = models.CharField(max_length=100)
    parking = models.CharField(max_length=3, choices=y_n_choices)
    balcony = models.CharField(max_length=3, choices=y_n_choices)
    individual = models.CharField(max_length=3, choices=y_n_choices)
    attached_bathroom = models.CharField(max_length=3, choices=y_n_choices)
    kitchen = models.CharField(max_length=15, choices=[('furnished', 'Furnished'), ('basic', 'Basic')])
    contact_time = models.CharField(max_length=50)  #will change to numeric type
    prefered_customer = models.CharField(max_length=20)
    gender_pref = models.CharField(max_length=10, choices=[('female', 'Female'), ('male', 'Male'), ('none', 'None')])
    Paying_guest = models.BooleanField()
    people_per_room = models.IntegerField()
    food = models.CharField(max_length=3, choices=[('included', 'Included'), ('not included', 'Not Included')])

    def __str__(self):
        return self.name


class Images(models.Model):
    user = models.ForeignKey(RentingUser, default=None, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='media/', verbose_name='Image')



