from django import forms
from django.contrib.auth import authenticate
from .models import User


class RegisterForm(forms.ModelForm):
    username = forms.CharField(
        label="Usuario",
        max_length=150,
        widget=forms.TextInput(
            attrs={"placeholder": "Usuario", "class": "form-control"}
        ),
    )
    email = forms.EmailField(
        label="Email",
        max_length=150,
        widget=forms.TextInput(attrs={"placeholder": "Email", "class": "form-control"}),
    )
    first_name = forms.CharField(
        label="Nombre",
        max_length=30,
        widget=forms.TextInput(
            attrs={"placeholder": "Nombre", "class": "form-control"}
        ),
    )
    last_name = forms.CharField(
        label="Apellido",
        max_length=30,
        widget=forms.TextInput(
            attrs={"placeholder": "Apellido", "class": "form-control"}
        ),
    )
    password1 = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(
            attrs={"placeholder": "Contraseña", "class": "form-control"}
        ),
    )
    password2 = forms.CharField(
        label="Confirme su contraseña",
        widget=forms.PasswordInput(
            attrs={"placeholder": "Confirmar contraseña", "class": "form-control"}
        ),
    )

    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
        ]  # Agrega campos según tu modelo

    def clean_email(self):
        email = self.cleaned_data["email"]
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Este correo ya está en uso.")
        return email

    def clean_password2(self):
        pw1 = self.cleaned_data.get("password1")
        pw2 = self.cleaned_data.get("password2")
        if pw1 and pw2 and pw1 != pw2:
            raise forms.ValidationError("Las contraseñas no coinciden.")
        return pw2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    username = forms.CharField(
        label="Usuario",
        max_length=150,
        widget=forms.TextInput(
            attrs={"placeholder": "Usuario", "class": "form-control"}
        ),
    )
    password = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(
            attrs={"placeholder": "Contraseña", "class": "form-control"}
        ),
    )

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        password = cleaned_data.get("password")

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError("Credenciales inválidas.")
            cleaned_data["user"] = user
        return cleaned_data
