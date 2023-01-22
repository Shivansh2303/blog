from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User


class UserModel(models.Model):
    username=models.CharField(max_length=255,blank=False,null=False)
    email=models.EmailField(unique=True,max_length=200)
    password=models.CharField(blank=False,null=False,max_length=255)
    profile_image=models.ImageField()
    is_active=models.BooleanField(default=False)
    # date_joined=models.DateTimeField()

