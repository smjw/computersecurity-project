from django.db import models
from django.contrib.auth.models import *
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.
 
class Customer(AbstractUser):
    email = models.EmailField(("email address"), unique=True, null=False, blank=False)
    first_name = models.CharField(max_length=50, null=False, blank=False)
    last_name = models.CharField(max_length=50, null=False, blank=False)
    phone_number = PhoneNumberField(unique=True, null=False, blank=False)


    REQUIRED_FIELDS = ("email", "first_name", "last_name", "phone_number")

    def __str__(self):
        return self.username
