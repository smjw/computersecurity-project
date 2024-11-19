from django.urls import path
from . import views  # Import the views from the users app

urlpatterns = [
    path('register/', views.register, name='register'),  # Register URL mapped to the 'register' view
]
