from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save


# from main.models import Location
# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=181, blank=True)
    title = models.CharField(max_length=10, blank=True, choices=[('Mr.', 'Mr.'), ('Ms.', 'Ms.'), ], default='')
    mobile_no = models.CharField(null=True, blank=True, max_length=12)
    email = models.EmailField(max_length=70, null=True, blank=True)
    verified = models.BooleanField(default=False)
    email_verified = models.BooleanField(default=False)
    session_id = models.CharField(max_length=181, blank=True)
    shop_owner = models.BooleanField(default=False)
    location = models.ForeignKey('main.Location', on_delete=models.CASCADE, null=True)

    def is_verified(self):

        if self.verified:
            return True
        else:
            return False

    def is_shop_owner(self):
        return self.shop_owner


def create_profile(sender, **kwargs):
    user = kwargs["instance"]
    if kwargs["created"]:
        user_profile = Profile(user=user)
        user_profile.name = user.get_full_name()
        user_profile.email = user.email
        user_profile.save()


post_save.connect(create_profile, sender=User)
