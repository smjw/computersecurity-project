from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Customer

class CustomerRegistrationForm(UserCreationForm):
    security_answer = forms.CharField(
        label="Security Question: What is your mother's maiden name?",
        widget=forms.TextInput(attrs={'placeholder':'enter answer'}),
    )
    class Meta:
        model = Customer
        fields = ["username", "email", "first_name", "last_name", "phone_number", "password1", "password2", "security_answer"]
