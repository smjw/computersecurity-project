from django.shortcuts import render, redirect
from .forms import CustomerRegistrationForm

# Create your views here.

def register(request):
    if request.method == "POST":
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")#redirect later
    else:
        form = CustomerRegistrationForm()
    return render(request, "customers/register.html", {"form":form})