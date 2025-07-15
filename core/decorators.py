from django_otp.plugins.otp_totp.models import TOTPDevice
from django.shortcuts import redirect
from functools import wraps


def require_totp_confirmed(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated:
            confirmed = TOTPDevice.objects.filter(
                user=request.user, confirmed=True
            ).exists()
            if not confirmed:
                return redirect("setup_totp_manual")
        return view_func(request, *args, **kwargs)

    return _wrapped_view
