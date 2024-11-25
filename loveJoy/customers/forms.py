from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Customer

class CustomerRegistrationForm(UserCreationForm):
    class Meta:
        model = Customer
        fields = ["username", "email", "first_name", "last_name", "phone_number", "password1", "password2"]
