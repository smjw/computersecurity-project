from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    firstname = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    contact_number = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return self.username
