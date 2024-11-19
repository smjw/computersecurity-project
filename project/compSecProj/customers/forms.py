from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    contact_number = forms.CharField(max_length=15)

    class Meta:
        model = CustomUser
        fields = ['firstname','surname','username', 'email', 'password', 'contact_number']
