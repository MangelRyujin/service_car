from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator



# Create your models here.

class User(AbstractUser):
    email = models.EmailField("Email", blank=False,null=False,unique=True)
    phone_number = models.CharField("Phone number",max_length=20,null=True,blank=True)
    country = models.CharField("Country", max_length=255,null=True,blank=True)
    city = models.CharField("Country",max_length=255, null=True,blank=True)
    address = models.CharField("Address",max_length=255, null=True,blank=True)
    dni = models.CharField("DNI",max_length=20,unique=True, null=True,blank=True)
    