from django.db import models
import os
from django.utils.text import slugify


def logo_upload_path(instance, filename):
    ext = os.path.splitext(filename)[1]
    new_filename = slugify(instance.short_name) + ext
    return f"clients/logos/{new_filename}"


class Client(models.Model):
    name = models.CharField(max_length=255, verbose_name="Nombre del Cliente")
    short_name = models.CharField(max_length=50, verbose_name="Nombre Corto")
    industry = models.CharField(max_length=100, blank=True)
    logo = models.ImageField(upload_to=logo_upload_path, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def get_logo_url(self):
        if self.logo:
            return self.logo.url
        return "/static/img/default_logo.png"

    def __str__(self):
        return self.name


class Contact(models.Model):
    first_name = models.CharField(max_length=100, verbose_name="Nombre")
    last_name = models.CharField(max_length=100, verbose_name="Apellido")
    role = models.CharField(max_length=150, verbose_name="Cargo")
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=50, blank=True)
    client = models.ForeignKey(
        Client, on_delete=models.CASCADE, related_name="contacts"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} {self.email}"
