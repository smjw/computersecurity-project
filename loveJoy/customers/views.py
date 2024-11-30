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
from django.contrib.auth import get_user_model
from .models import Customer
from django.contrib.auth.decorators import login_required
from .forms import EvaluationRequestForm
from .models import RequestList
from django.contrib.auth.decorators import user_passes_test


def register(request):
    if request.method == "POST":
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
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
                return redirect("request_evaluation")  # redirect
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
                customer = Customer.objects.get(email=email)
                if customer.security_answer == security_answer:  
                    return redirect('password_reset')
                else:
                    form.add_error('security_answer', 'Incorrect security answer.')
            except Customer.DoesNotExist:
                form.add_error('email', 'Email address not found.')

    else:
        form = PasswordResetForm()

    return render(request, 'customers/securitycheck.html', {'form': form})


def request_evaluation(request):
    if request.method == 'POST':
        form = EvaluationRequestForm(request.POST, request.FILES)
        if form.is_valid():
            evaluation_request = form.save(commit=False)
            evaluation_request.user = request.user
            evaluation_request.save()
            return redirect('evaluation_success')  
    else:
        form = EvaluationRequestForm()
    return render(request, 'customers/request_evaluation.html', {'form': form})


def evaluation_success(request):
    return render(request, 'customers/evaluation_success.html')


#check if admin
def admin_required(view_func):
    return user_passes_test(lambda u: u.is_superuser)(view_func)

@admin_required
def admin_request_list(request):
    requests = RequestList.objects.all().order_by("-submitted_at")
    return render(request, "admin_request_list.html", {"requests": requests})
