from django.db import models
from django.core.validators import MinLengthValidator
from projects.models import Project
from core.utils import generate_vuln_code


class VulnerabilityCategory(models.Model):
    name = models.CharField("Nombre de la categoría", max_length=100, unique=True)
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

    def __str__(self):
        return f"{self.code} {self.name}" if self.code else self.name


class Vulnerability(models.Model):
    REMEDIATION_CHOICES = [("low", "Low"), ("medium", "Medium"), ("high", "High")]
    PRIORITY_CHOICES = [
        ("low", "Low"),
        ("medium", "Medium"),
        ("high", "High"),
        ("urgent", "Urgent"),
    ]
    RISK_COMPONENT_CHOICES = [("low", "Baja"), ("medium", "Media"), ("high", "Alta")]

    title = models.CharField(max_length=255, validators=[MinLengthValidator(5)])
    category = models.ForeignKey(VulnerabilityCategory, on_delete=models.PROTECT)
    vuln_type = models.ForeignKey(VulnerabilityType, on_delete=models.PROTECT)
    description = models.TextField("Descripción", validators=[MinLengthValidator(20)])

    cvss_31_vector = models.CharField(
        "CVSS 3.1 Vector", max_length=255, blank=True, null=True
    )
    cvss_31_score = models.DecimalField(
        "CVSS 3.1 Score",
        max_digits=4,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Puntaje numérico calculado del vector CVSS 3.1",
    )
    cvss_31_severity = models.CharField(
        "Severidad CVSS 3.1",
        max_length=20,
        blank=True,
        help_text="Severidad estimada según el score: None, Low, Medium, High, Critical",
    )

    cvss_40_vector = models.CharField(
        "CVSS 4.0 Vector", max_length=255, blank=True, null=True
    )
    cvss_40_score = models.DecimalField(
        "CVSS 4.0 Score",
        max_digits=4,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Puntaje numérico calculado del vector CVSS 4.0",
    )
    cvss_40_severity = models.CharField(
        "Severidad CVSS 4.0",
        max_length=20,
        blank=True,
        help_text="Severidad estimada según el score: None, Low, Medium, High, Critical",
    )

    remediation = models.TextField("Remediación", validators=[MinLengthValidator(20)])
    remediation_complexity = models.CharField(
        "Complejidad", choices=REMEDIATION_CHOICES, max_length=10
    )
    remediation_priority = models.CharField(
        "Prioridad", choices=PRIORITY_CHOICES, max_length=10
    )
    impact = models.CharField("Impacto", choices=RISK_COMPONENT_CHOICES, max_length=10)
    likelihood = models.CharField(
        "Probabilidad", choices=RISK_COMPONENT_CHOICES, max_length=10
    )

    risk_rating = models.CharField("Riesgo OWASP", max_length=10, editable=False)
    references = models.TextField(
        "Referencias",
        help_text="Una por línea: CWE-79, CVE-2024-12345, OWASP A01, PCI-DSS Req 6.6...",
    )
    created_at = models.DateTimeField(auto_now_add=True)

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


class ProjectVulnerability(models.Model):
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="vulnerabilities", null=True
    )
    vulnerability = models.ForeignKey(Vulnerability, on_delete=models.CASCADE)
    vulnerability_type = models.CharField(max_length=50)  # Ej: "web"
    vuln_code = models.CharField(max_length=100, editable=False, unique=True)

    status = models.CharField(
        max_length=50,
        choices=[
            ("abierta", "Abierta"),
            ("en_proceso", "En Proceso"),
            ("mitigada", "Mitigada"),
        ],
    )
    location = models.CharField(
        max_length=255,
        blank=True,
        help_text="Ej: /login, /admin, bucket S3, servidor vulnerable...",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.vuln_code

    def save(self, *args, **kwargs):
        if not self.vuln_code:
            self.vuln_code = generate_vuln_code(self.project, self.vulnerability_type)
        super().save(*args, **kwargs)


class Evidence(models.Model):
    project_vulnerability = models.ForeignKey(
        ProjectVulnerability,
        on_delete=models.CASCADE,
        related_name="evidences",
        null=True,
    )
    image = models.ImageField(upload_to="evidences/")
    caption = models.CharField(max_length=255, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
