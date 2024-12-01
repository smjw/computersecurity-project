from django.urls import path, include
from . import views
from .views import *
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView




urlpatterns = [
    path("", views.home, name="home"),
    path("register/", views.register, name="register"),
    path('captcha/', include('captcha.urls')),

    path("login/", user_login, name="login"),  
    path("logout/", LogoutView.as_view(), name="logout"),
    path('securitycheck/', views.password_reset, name='securitycheck'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='registration/password_reset_form.html'), name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset_complete'),
    path('request_evaluation/', request_evaluation, name='request_evaluation'),
    path('evaluation_success/', evaluation_success, name='evaluation_success'),
    path("admin/request_list/", admin_request_list, name="admin_request_list"),
    
]