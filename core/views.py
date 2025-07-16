from django.contrib.auth import login, logout
from django.contrib.auth.views import LogoutView
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django_otp.plugins.otp_totp.models import TOTPDevice
from .forms import LoginForm, RegisterForm
from django.contrib.auth.hashers import make_password
from .decorators import require_totp_confirmed
from .models import User

import qrcode
from qrcode.image.pil import PilImage
from io import BytesIO
import base64


# Paso 1: Login inicial (username + password)
def prelogin_view(request):
    form = LoginForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        user = form.cleaned_data["user"]
        request.session["preauth_user_id"] = user.id
        return redirect("verify_totp")

    return render(request, "core/login.html", {"form": form})


# Paso 2: Verificación del código 2FA (TOTP)
def verify_totp_view(request):
    user_id = request.session.get("preauth_user_id")
    if not user_id:
        return redirect("login")

    user = User.objects.filter(id=user_id).first()
    if not user:
        return redirect("login")

    # ⚠️ Verifica si NO tiene dispositivo TOTP confirmado
    has_totp = TOTPDevice.objects.filter(user=user, confirmed=True).exists()
    if not has_totp:
        login(request, user)  # ⚠️ Logueamos para que pueda crear su TOTP
        del request.session["preauth_user_id"]
        return redirect("setup_totp")

    # Si sí tiene TOTP confirmado, pedimos token
    device = TOTPDevice.objects.filter(user=user, confirmed=True).first()
    error = None

    if request.method == "POST":
        token = request.POST.get("token")
        if device and device.verify_token(token):
            login(request, user)
            del request.session["preauth_user_id"]
            return redirect("dashboard")
        else:
            error = "Código inválido. Intenta nuevamente."

    return render(request, "core/verify_totp.html", {"error": error})



# Paso 3: Setup de TOTP (escaneo QR + confirmación)
@login_required
def setup_totp_view(request):
    device, _ = TOTPDevice.objects.get_or_create(
        user=request.user,
        name="default",
        confirmed=False,
    )

    uri = device.config_url
    qr = qrcode.make(uri, image_factory=PilImage)
    buffer = BytesIO()
    qr.save(buffer, format="PNG")
    qr_base64 = base64.b64encode(buffer.getvalue()).decode()

    # 🔐 Clave manual en Base32
    base32_secret = base64.b32encode(device.bin_key).decode("utf-8")

    if request.method == "POST":
        token = request.POST.get("token")
        if device.verify_token(token):
            device.confirmed = True
            device.save()
            return redirect("dashboard")
        else:
            return render(
                request,
                "core/setup_totp.html",
                {
                    "qr": f"data:image/png;base64,{qr_base64}",
                    "secret": base32_secret,
                    "error": "Código inválido. Intenta nuevamente.",
                },
            )

    return render(
        request,
        "core/setup_totp.html",
        {
            "qr": f"data:image/png;base64,{qr_base64}",
            "secret": base32_secret,
        },
    )




# Paso 4: Dashboard protegido
@login_required
@require_totp_confirmed
def dashboard_view(request):
    return render(request, "core/dashboard.html", {"user": request.user})


# Paso 5: Logout
class UserLogoutView(LogoutView):
    next_page = "login"


# Registro de usuario
def register_view(request):
    form = RegisterForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        user = form.save(commit=False)
        user.password = make_password(form.cleaned_data["password"])
        user.save()
        return redirect("login")  # Opcional: redirige a login tras registro exitoso

    return render(request, "core/user_register.html", {"form": form})