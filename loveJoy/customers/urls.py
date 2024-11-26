from django.urls import path
from . import views
from .views import *
from django.contrib.auth import views as auth_views


urlpatterns = [
    path("register/", views.register, name="register"),
    path("login/", user_login, name="login"),  
    path('password_reset/', views.password_reset, name='password_reset'),  # Custom security check
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

]