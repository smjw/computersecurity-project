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
from .models import Customer
from django.contrib.auth.decorators import login_required
from .forms import EvaluationRequestForm
from .models import EvaluationRequest
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode
from datetime import datetime, timedelta
from django.utils.timezone import now
from django_otp.plugins.otp_totp.models import TOTPDevice
from django.shortcuts import get_object_or_404
import random
from django.http import HttpResponseForbidden






# home page
def home(request):
    return render(request, "customers/home.html")


# registration 
def register(request):
    if request.method == "POST":
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # Deactivate the user until email verification
            user.save()

            # email verif token
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            domain = get_current_site(request).domain
            verification_link = reverse('email_verification', kwargs={'uidb64': uid, 'token': token})
            verification_url = f"http://{domain}{verification_link}"
            
            # send verification email
            send_mail(
                subject="Verify your email address",
                message=f"Click the link to verify your email: {verification_url}",
                from_email="email@gmail.com",
                recipient_list=[user.email],
            )
            
            return redirect("email_verification_sent")
        else: 
            print(form.errors)
    else:
        form = CustomerRegistrationForm()
    return render(request, "customers/register.html", {"form":form})


#email verification
def email_verification(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Customer.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return render(request, "customers/email_verification_success.html")
    else:
        return render(request, "customers/email_verification_failed.html")



# customer log in
def user_login(request):
    max_attempts = 3
    lockout_time = 10
    if request.method == 'POST':

        attempts = request.session.get('login_attempts', 0)
        lockout_until = request.session.get('lockout_until')

        if lockout_until:
            lockout_until = datetime.fromisoformat(lockout_until)  
            if now() < lockout_until:
                remaining_time = (lockout_until - now()).seconds // 60
                messages.error(request, f"Too many login attempts. Try again in {remaining_time} minutes.")
                return render(request, 'customers/login.html', {'form': CustomAuthenticationForm()})
        
        
        form = CustomAuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                # reset session 
                request.session['login_attempts'] = 0
                request.session['lockout_until'] = None
            
                
                otp = str(random.randint(100000, 999999))
                request.session['otp'] = otp
            
                # Send OTP email
                send_mail(
                    subject="Your OTP Code",
                    message=f"Your OTP code is {otp} It will expire in 5 minutes.",
                    from_email="email@gmail.com",  
                    recipient_list=[user.email],
                )

                # Store user id in session for later OTP validation
                request.session['pending_user_id'] = user.id

                # Redirect to OTP validation page
                return redirect('validate_otp')
            else:

                attempts += 1
                request.session['login_attempts'] = attempts
                messages.error(request, "Invalid username or password.")

        else:
            attempts += 1
            request.session['login_attempts'] = attempts
            messages.error(request,  f"Invalid username or password. You have {max_attempts - request.session["login_attempts"]} attempt(s) remaining.")

        #maxed out attempts
        if attempts >= max_attempts:
            lockout_until = now() + timedelta(minutes=lockout_time)
            request.session['lockout_until'] = lockout_until.isoformat()  # Store as string for session
            messages.error(request, f"Too many login attempts. Try again after {lockout_time} minutes.")
            return render(request, 'customers/login.html', {'form': CustomAuthenticationForm()})

    else:
        form = CustomAuthenticationForm()

    return render(request, 'customers/login.html', {'form': form})


# one time password for login
def validate_otp(request):
    user_id = request.session.get('pending_user_id')
    if not user_id:
        return HttpResponseForbidden("Unauthorized access")

    user = get_object_or_404(Customer, id=user_id)


    if request.method == 'POST':
        otp_token = request.POST.get('otp_token')

        # Vcheck
        if otp_token == request.session.get('otp'):
            # clear session
            del request.session['otp']
            del request.session['pending_user_id']
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid OTP. Please try again.")

    return render(request, 'customers/validate_otp.html')




# forgotten password
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



# user requests an evaluation
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


#check if admin, view list of requests
def admin_required(view_func):
    return user_passes_test(lambda u: u.is_superuser)(view_func)

@admin_required
def admin_request_list(request):
    requests = EvaluationRequest.objects.all().order_by
    return render(request, "customers/admin_request_list.html", {"requests": requests})

