from django import forms
from django.core.exceptions import ValidationError
import os
from .models import Client, Contact


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ["name", "short_name", "industry", "logo"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "short_name": forms.TextInput(attrs={"class": "form-control"}),
            "industry": forms.TextInput(attrs={"class": "form-control"}),
            "logo": forms.ClearableFileInput(attrs={"class": "form-control"}),
        }

    def clean_logo(self):
        logo = self.cleaned_data.get("logo")
        if logo:
            valid_types = ["image/png", "image/jpeg", "image/svg+xml"]
            if logo.content_type not in valid_types:
                raise ValidationError(
                    "Archivo no válido. Solo imágenes PNG, JPG, JPEG o SVG."
                )
        return logo


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ["first_name", "last_name", "role", "email", "phone", "client"]
        widgets = {
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "role": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "phone": forms.TextInput(attrs={"class": "form-control"}),
            "client": forms.Select(attrs={"class": "form-control"}),
        }
