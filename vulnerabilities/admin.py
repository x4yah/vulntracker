from django.contrib import admin
from django.utils.html import format_html
from .models import (
    Vulnerability,
    VulnerabilityCategory,
    VulnerabilityType,
    ProjectVulnerability,
    Evidence,
)


@admin.register(VulnerabilityCategory)
class VulnerabilityCategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "standard"]
    search_fields = ["name", "standard"]


@admin.register(VulnerabilityType)
class VulnerabilityTypeAdmin(admin.ModelAdmin):
    list_display = ["code", "name", "category"]
    search_fields = ["code", "name"]
    list_filter = ["category"]


@admin.register(Vulnerability)
class VulnerabilityAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "vuln_type",
        "cvss_31_score",
        "colored_severity",
        "risk_rating",
        "created_at",
    ]
    list_filter = [
        "risk_rating",
        "impact",
        "likelihood",
        "cvss_31_severity",
        "remediation_priority",
    ]
    search_fields = ["title", "description", "references"]
    readonly_fields = ["risk_rating", "cvss_31_severity", "cvss_40_severity"]
    list_select_related = ["vuln_type"]
    date_hierarchy = "created_at"

    def colored_severity(self, obj):
        severity = obj.cvss_31_severity or obj.cvss_40_severity or "—"
        color = {
            "critical": "darkred",
            "high": "orangered",
            "medium": "orange",
            "low": "gray",
            "none": "green",
        }.get(severity.lower(), "black")
        return format_html(f'<b style="color:{color}">{severity}</b>')

    colored_severity.short_description = "Severidad CVSS"


@admin.register(ProjectVulnerability)
class ProjectVulnerabilityAdmin(admin.ModelAdmin):
    list_display = [
        "vuln_code",
        "project",
        "vulnerability",
        "status",
        "location",
        "created_at",
    ]
    list_filter = ["status", "project"]
    search_fields = ["vuln_code", "project__name", "vulnerability__title"]
    date_hierarchy = "created_at"
    list_select_related = ["project", "vulnerability"]


@admin.register(Evidence)
class EvidenceAdmin(admin.ModelAdmin):
    list_display = ["project_vulnerability", "image", "caption", "uploaded_at"]
    search_fields = ["caption", "project_vulnerability__vuln_code"]
    list_filter = ["uploaded_at"]
