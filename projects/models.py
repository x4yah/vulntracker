from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from customers.models import Client

User = get_user_model()


class Project(models.Model):
    name = models.CharField(max_length=100)
    code_name = models.SlugField(max_length=50, unique=True)  # Ej: coconut-atlantis
    description = models.TextField("Descripción general", blank=True)
    scope = models.TextField("Alcance del proyecto", blank=True)
    client = models.ForeignKey(
        Client, on_delete=models.CASCADE, related_name="projects"
    )
    # 🧠 Responsable principal
    leader = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="projects_led",
    )

    # 👥 Colaboradores adicionales
    specialist = models.ManyToManyField(
        settings.AUTH_USER_MODEL, blank=True, related_name="projects_collaborated"
    )
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    status = models.CharField(
        max_length=50,
        choices=[
            ("por_iniciar", "Por iniciar"),
            ("activo", "Activo"),
            ("on_hold", "En pausa"),
            ("en_progreso", "En Progreso"),
            ("retrasado", "Retrasado"),
            ("cerrado", "Cerrado"),
        ],
    )
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
