from django.urls import path
from django.contrib.auth import views as auth_views

from .views import *

urlpatterns = [
    # Authenticaion
    path('register/', register_user, name='register'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),

    # Account Activation
    path('activate-user/<uidb64>/<token>/', activateUser, name='activate_user'),
    path('generate-link/', generateLink, name='generate_link'),

    # Change Password
    path('change-password/', change_password, name='change_password'),

    # Password Reset
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='accounts/password_reset.html'), name="password_reset"),
    path('password-reset-done/', auth_views.PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html'), name="password_reset_done"),
    path('password-reset-confirm/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(
    template_name='accounts/password_reset_confirm.html'), name="password_reset_confirm"),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'), name="password_reset_complete"),
]