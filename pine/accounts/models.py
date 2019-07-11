from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save


# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=181, blank=True)
    title = models.CharField(max_length= 10 ,blank=True, choices=[('Mr.', 'Mr.'),('Ms.', 'Ms.'),],default='')
    mobile_no = models.IntegerField(null=True, blank=True, unique=True)
    email = models.EmailField(max_length=70, null=True, blank=True)
    verified = models.BooleanField(default=False)
    email_verified = models.BooleanField(default=False)
    session_id = models.CharField(max_length=181, blank=True)


    def is_verified(self):

        if self.verified:
            return True
        else:
            return False


def create_profile(sender, **kwargs):
    user = kwargs["instance"]
    if kwargs["created"]:
        user_profile = Profile(user=user)
        user_profile.name = user.get_full_name()
        user_profile.email = user.email

        user_profile.save()


post_save.connect(create_profile, sender=User)