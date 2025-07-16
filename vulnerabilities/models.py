from django.db import models
from django.core.validators import MinLengthValidator
# Create your models here.


class VulnerabilityCategory(models.Model):
    name = models.CharField("Nombre de la categoría", max_length=100, unique=True)

    # Ej: "Web", "Mobile", "Wireless"
    standard = models.TextField(
        "Marco de referencia",
        blank=True,
        help_text="Ej: OWASP Top 10 2021, OWISAM Top 10",
    )

    def __str__(self):
        return self.name


class VulnerabilityType(models.Model):
    category = models.ForeignKey(
        VulnerabilityCategory, on_delete=models.CASCADE, related_name="types"
    )
    code = models.CharField("Código", max_length=50, blank=True)
    name = models.CharField("Nombre", max_length=150)

    # Ej: OWISAM-TR-004, A01:2021-Injection, etc.

    def __str__(self):
        return f"{self.code} {self.name}" if self.code else self.name


class Vulnerability(models.Model):
    CATEGORY_CHOICES = [
        ("web", "Web"),
        ("mobile", "Mobile"),
        ("network", "Network"),
        ("wireless", "Wireless"),
        ("cloud", "Cloud"),
        ("attack_surface", "Attack Surface"),
        ("otro", "Otro"),
    ]

    REMEDIATION_CHOICES = [
        ("low", "Low"),
        ("medium", "Medium"),
        ("high", "High"),
    ]

    PRIORITY_CHOICES = [
        ("low", "Low"),
        ("medium", "Medium"),
        ("high", "High"),
        ("urgent", "Urgent"),
    ]

    RISK_COMPONENT_CHOICES = [
        ("low", "Baja"),
        ("medium", "Media"),
        ("high", "Alta"),
    ]
    title = models.CharField(max_length=255, validators=[MinLengthValidator(5)])
    category = models.ForeignKey(VulnerabilityCategory, on_delete=models.PROTECT)
    vuln_type = models.ForeignKey(VulnerabilityType, on_delete=models.PROTECT)
    description = models.TextField("Descripción", validators=[MinLengthValidator(20)])
    cvss_31_vector = models.CharField(
        "CVSS 3.1 Vector", max_length=255, blank=True, null=True
    )
    cvss_40_vector = models.CharField(
        "CVSS 4.0 Vector", max_length=255, blank=True, null=True
    )
    remediation = models.TextField("Remediación", validators=[MinLengthValidator(20)])
    remediation_complexity = models.CharField(
        "Complejidad de Remediación", choices=REMEDIATION_CHOICES
    )
    remediation_priority = models.CharField(
        "Prioridad", max_length=10, choices=PRIORITY_CHOICES
    )

    impact = models.CharField("Impacto", max_length=10, choices=RISK_COMPONENT_CHOICES)
    likelihood = models.CharField(
        "Probabilidad", max_length=10, choices=RISK_COMPONENT_CHOICES
    )

    risk_rating = models.CharField(
        "Riesgo OWASP", max_length=10, editable=False
    )  # Calculado en `save()`
    proof_image = models.ImageField(
        "Captura / PoC",
        upload_to="vulnerabilities/",
        blank=True,
        null=True,
        help_text="Imagen o screenshot que evidencia la vulnerabilidad.",
    )
    references = models.TextField(
        "Referencias",
        help_text="Una por línea: CWE-79, CVE-2024-12345, OWASP A01, PCI-DSS Req 6.6...",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=50,
        choices=[
            ("open", "Open"),
            ("in_progress", "In Progress"),
            ("resolved", "Resolved"),
            ("closed", "Closed"),
        ],
    )

    def save(self, *args, **kwargs):
        if self.impact and self.likelihood:
            risk_matrix = {
                ("low", "low"): "low",
                ("low", "medium"): "medium",
                ("low", "high"): "medium",
                ("medium", "low"): "medium",
                ("medium", "medium"): "medium",
                ("medium", "high"): "high",
                ("high", "low"): "medium",
                ("high", "medium"): "high",
                ("high", "high"): "critical",
            }
            key = (self.impact, self.likelihood)
            self.risk_rating = risk_matrix.get(key, "medium")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} ({self.category})"
