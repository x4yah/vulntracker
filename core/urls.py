# core/urls.py

from django.urls import path
from .views import (
    dashboard_view,
    user_logout_view,
    setup_totp_manual,
    login_view,
    User_Register_View,
)

urlpatterns = [
    path("dashboard/", dashboard_view, name="dashboard"),
    path("logout/", user_logout_view.as_view(), name="logout"),
    path("setup/totp/", setup_totp_manual, name="setup_totp_manual"),
    path("login/", login_view, name="login"),
    path("register/", User_Register_View.as_view(), name="register"),
    
]
