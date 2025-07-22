from django.contrib import admin
from .models import Client, Contact


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ["name", "short_name"]
    search_fields = ["name", "short_name"]


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ["first_name", "last_name", "role", "email", "client"]
    search_fields = ["first_name", "last_name", "email"]
    list_filter = ["client"]


class ClientAdmin(admin.ModelAdmin):
    list_display = ["name", "short_name", "user_count"]
    search_fields = ["name", "short_name"]

    def user_count(self, obj):
        return obj.users.count()

    user_count.short_description = "Usuarios vinculados"
