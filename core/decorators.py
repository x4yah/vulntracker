from django.shortcuts import redirect
from django_otp.plugins.otp_totp.models import TOTPDevice


def require_totp_confirmed(view_func):
    def wrapped_view(request, *args, **kwargs):
        if not TOTPDevice.objects.filter(user=request.user, confirmed=True).exists():
            return redirect("setup_totp")
        return view_func(request, *args, **kwargs)

    return wrapped_view
