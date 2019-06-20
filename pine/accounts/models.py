from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length = 181, blank=True)
    mobile_no = models.IntegerField(null=True, blank=True, unique=True)
    email = models.EmailField(max_length=70, null=True, blank=True, unique=True)
    verified = models.BooleanField(default=False)
    


    def __str__(self):
        return self.user.username
