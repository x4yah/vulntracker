from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Role
from .forms import RegisterForm


# Register your models here.
class UserAdmin(BaseUserAdmin):
    add_form = RegisterForm
    model = User
    list_display = ("email", "first_name", "last_name", "job_title", "role", "is_staff")
    list_filter = ("role", "is_staff")
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            "Información personal",
            {"fields": ("first_name", "last_name", "job_title", "role", "totp_secret")},
        ),
        (
            "Permisos",
            {
                "fields": (
                    "is_staff",
                    "is_superuser",
                    "is_active",
                    "groups",
                    "user_permissions",
                )
            },
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "first_name",
                    "last_name",
                    "email",
                    "job_title",
                    "role",
                    "totp_secret",
                    "password1",
                    "password2",
                ),
            },
        ),
    )
    search_fields = ("email",)
    ordering = ("email",)


admin.site.register(User, UserAdmin)
admin.site.register(Role)
