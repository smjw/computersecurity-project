from django.shortcuts import render, redirect
from .forms import CustomerRegistrationForm
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .forms import CustomAuthenticationForm
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from .forms import PasswordResetForm

# Create your views here.

def register(request):
    if request.method == "POST":
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")#redirect later
        else: 
            print(form.errors)
    else:
        form = CustomerRegistrationForm()
    return render(request, "customers/register.html", {"form":form})

def user_login(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome, {user.username}!")
                return redirect('home')  # redirect
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Please correct the error below.")
    else:
        form = CustomAuthenticationForm()

    return render(request, 'customers/login.html', {'form': form})


def password_reset(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            security_answer = form.cleaned_data['security_answer']

            try:
                user = User.objects.get(email=email)
                if user.profile.security_answer == security_answer:
                    # Redirect to the Django password reset view if the security answer is correct
                    return redirect('password_reset')  # redirect to Django's built-in password reset view
                else:
                    messages.error(request, 'Incorrect security answer.')
            except User.DoesNotExist:
                messages.error(request, 'Email address not found.')

    else:
        form = PasswordResetForm()

    return render(request, 'customers/securitycheck.html', {'form': form})