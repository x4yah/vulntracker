from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.contrib.auth import login
from django.contrib.auth.views import LogoutView
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django_otp.plugins.otp_totp.models import TOTPDevice
from core.decorators import require_totp_confirmed
from .forms import UserCreationForm, login_form
from .models import User
import qrcode
from qrcode.image.pil import PilImage 
from io import BytesIO
import base64

@login_required
def setup_totp_manual(request):
    device, _ = TOTPDevice.objects.get_or_create(
        user=request.user,
        name="default",
        confirmed=False
    )
    uri = device.config_url
    qr = qrcode.make(uri, image_factory=PilImage)
    buffer = BytesIO()
    qr.save(buffer, format="PNG")  # ahora sí funciona
    qr_base64 = base64.b64encode(buffer.getvalue()).decode()

    if request.method == "POST":
        token = request.POST.get("token")
        if device.verify_token(token):
            device.confirmed = True
            device.save()
            return redirect("dashboard")
        else:
            return render(request, "core/setup_totp.html", {
    "qr": f"data:image/png;base64,{qr_base64}",
    "error": "Código inválido",
    "secret": device.key
})


    return render(request, "core/setup_totp.html", {
    "qr": f"data:image/png;base64,{qr_base64}",
    "secret": device.key
})


class user_logout_view(LogoutView):
    next_page = reverse_lazy("login")

class User_Register_View(CreateView):
    model = User
    form_class = UserCreationForm
    template_name = "core/user_register.html"
    success_url = reverse_lazy("login")

@login_required
@require_totp_confirmed
def dashboard_view(request):
    user = request.user
    role = user.role.name if user.role else "Sin rol"
    return render(request, "core/dashboard.html", {"user": user, "role": role})

def login_view(request):
    if request.method == "POST":
        form = login_form(request.POST)
        if form.is_valid():
            user = form.cleaned_data["user"]
            login(request, user)
            device_qs = TOTPDevice.objects.filter(user=user)
            if not device_qs.filter(confirmed=True).exists():
                return redirect("setup_totp_manual")  # 👈 fallback personalizado
            return redirect("dashboard")
    else:
        form = login_form()
    return render(request, "core/login.html", {"form": form})
