from django.db import models
from django.contrib.auth.models import *
from phonenumber_field.modelfields import PhoneNumberField
from django.conf import settings
#from encrypted_model_fields.fields import EncryptedCharField, EncryptedTextField




# customer model
class Customer(AbstractUser):
    email = models.EmailField(("email address"), unique=True, null=False, blank=False)
    first_name = models.CharField(max_length=50, null=False, blank=False)
    last_name = models.CharField(max_length=50, null=False, blank=False)
    phone_number = PhoneNumberField(unique=True, null=False, blank=False, region='GB')
    security_answer = models.CharField(max_length=255, null=False, blank=False)


    REQUIRED_FIELDS = ("email", "first_name", "last_name", "phone_number", "security_answer")

    def __str__(self):
        return self.username
   

# user requests an evaluation
class EvaluationRequest(models.Model):
    CONTACT_METHOD_CHOICES = [
        ('phone', 'Phone'),
        ('email', 'Email'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    details = models.TextField()
    contact_method = models.CharField(max_length=10, choices=CONTACT_METHOD_CHOICES)
    photo = models.ImageField(upload_to='evaluation_photos/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Evaluation Request by {self.user.username} on {self.created_at}"
    


# admin views list of eval requests
class RequestList(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="evaluation_requests")
    comment = models.TextField()
    contact_method = models.CharField(max_length=10, choices=[("phone", "Phone"), ("email", "Email")])
    photo = models.ImageField(upload_to="evaluation_photos/")
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Request by {self.user} on {self.submitted_at}"
    


