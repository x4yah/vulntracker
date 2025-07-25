# Generated by Django 5.2.4 on 2025-07-16 16:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Client",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(max_length=255, verbose_name="Nombre del Cliente"),
                ),
                (
                    "short_name",
                    models.CharField(max_length=50, verbose_name="Nombre Corto"),
                ),
                (
                    "logo",
                    models.ImageField(
                        upload_to="clients/logos/", verbose_name="Logo Cliente"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Contact",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("first_name", models.CharField(max_length=100, verbose_name="Nombre")),
                (
                    "last_name",
                    models.CharField(max_length=100, verbose_name="Apellido"),
                ),
                ("role", models.CharField(max_length=150, verbose_name="Cargo")),
                ("email", models.EmailField(max_length=254, unique=True)),
                ("phone", models.CharField(blank=True, max_length=50)),
                (
                    "client",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="contacts",
                        to="customers.client",
                    ),
                ),
            ],
        ),
    ]
