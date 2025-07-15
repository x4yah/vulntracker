from django import template
from django_otp.plugins.otp_totp.models import TOTPDevice

register = template.Library()


@register.filter
def has_confirmed_totp(user):
    if not user.is_authenticated:
        return False
    return TOTPDevice.objects.filter(user=user, confirmed=True).exists()
