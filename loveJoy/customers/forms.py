from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Customer
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from .models import EvaluationRequest
from captcha.fields import CaptchaField
from django.core.exceptions import ValidationError
import os






# customer registers
class CustomerRegistrationForm(UserCreationForm):
    security_answer = forms.CharField(
        label="Security Question: What is your mother's maiden name?",
        widget=forms.TextInput(attrs={'placeholder':'enter answer'}),
    )
    captcha = CaptchaField()


    class Meta:
        model = Customer
        fields = ["username", "email", "first_name", "last_name", "phone_number", "password1", "password2", "security_answer"]


#customer logs in
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

# customer forgot password
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



#customer requests evaluation
class EvaluationRequestForm(forms.ModelForm):
    class Meta:
        model = EvaluationRequest
        fields = ['details', 'contact_method', 'photo']
        widgets = {
            'details': forms.Textarea(attrs={'placeholder': 'Enter details about the object...'}),
            'contact_method': forms.Select(),
        }
    def clean_photo(self):
        photo = self.cleaned_data.get('photo')

        # file size
        max_file_size = 5 * 1024 * 1024  # 5 MB
        if photo.size > max_file_size:
            raise ValidationError("The file is too large. Maximum size allowed is 5 MB.")

        # file type
        allowed_file_types = ['image/jpeg', 'image/png']
        if photo.content_type not in allowed_file_types:
            raise ValidationError("Unsupported file type. Please upload a JPEG or PNG image.")

        return photo

