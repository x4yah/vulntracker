from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.prelogin_view, name="login"),
    path("verify-totp/", views.verify_totp_view, name="verify_totp"),
    path("setup-totp/", views.setup_totp_view, name="setup_totp"),
    path("dashboard/", views.dashboard_view, name="dashboard"),
    path("logout/", views.UserLogoutView.as_view(), name="logout"),
    path("register/", views.register_view, name="register"),
    
]
