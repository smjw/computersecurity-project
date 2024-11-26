from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Customer
#from phonenumbers import parse, is_valid_number, NumberParseException
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User




class CustomerRegistrationForm(UserCreationForm):
    security_answer = forms.CharField(
        label="Security Question: What is your mother's maiden name?",
        widget=forms.TextInput(attrs={'placeholder':'enter answer'}),
    )
    class Meta:
        model = Customer
        fields = ["username", "email", "first_name", "last_name", "phone_number", "password1", "password2", "security_answer"]

    
class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
        label="Username",
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
        label="Password",
    )


class PasswordResetForm(forms.Form):
    email = forms.EmailField()
    security_answer = forms.CharField(max_length=255)

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        security_answer = cleaned_data.get("security_answer")

        try:
            customer = Customer.objects.get(email=email)
            if customer.security_answer != security_answer:  
                raise forms.ValidationError("Incorrect security answer.")
        except Customer.DoesNotExist:
            raise forms.ValidationError("Email address not found.")

        return cleaned_data

