from django import forms
from tinymce.widgets import TinyMCE
from .models import Vulnerability, VulnerabilityType, ProjectVulnerability


class ProjectVulnerabilityForm(forms.ModelForm):
    class Meta:
        model = ProjectVulnerability
        fields = "__all__"

        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "category": forms.Select(attrs={"class": "form-select"}),
            "vuln_type": forms.Select(attrs={"class": "form-select"}),
            # 🔁 Campos con TinyMCE
            "description": TinyMCE(attrs={"cols": 80, "rows": 20}),
            "remediation": TinyMCE(attrs={"cols": 80, "rows": 20}),
            "references": TinyMCE(attrs={"cols": 80, "rows": 20}),
            "cvss_31_vector": forms.TextInput(attrs={"class": "form-control"}),
            "cvss_31_score": forms.NumberInput(
                attrs={"class": "form-control", "step": "0.1", "min": "0", "max": "10"}
            ),
            "cvss_31_severity": forms.TextInput(
                attrs={"class": "form-control", "readonly": "readonly"}
            ),
            "cvss_40_vector": forms.TextInput(attrs={"class": "form-control"}),
            "cvss_40_score": forms.NumberInput(
                attrs={"class": "form-control", "step": "0.1", "min": "0", "max": "10"}
            ),
            "cvss_40_severity": forms.TextInput(
                attrs={"class": "form-control", "readonly": "readonly"}
            ),
            "remediation_complexity": forms.Select(attrs={"class": "form-select"}),
            "remediation_priority": forms.Select(attrs={"class": "form-select"}),
            "impact": forms.Select(attrs={"class": "form-select"}),
            "likelihood": forms.Select(attrs={"class": "form-select"}),
            "risk_rating": forms.TextInput(
                attrs={"class": "form-control", "readonly": "readonly"}
            ),
            "proof_image": TinyMCE(attrs={"cols": 80, "rows": 20}),
            "location": forms.TextInput(attrs={"class": "form-control"}),
            "project": forms.Select(attrs={"class": "form-select"}),
            "client": forms.Select(attrs={"class": "form-select"}),
            "status": forms.Select(attrs={"class": "form-select"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["vuln_type"].queryset = VulnerabilityType.objects.none()

        if "category" in self.data:
            try:
                category_id = int(self.data.get("category"))
                self.fields["vuln_type"].queryset = VulnerabilityType.objects.filter(
                    category_id=category_id
                )
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            if self.instance.category:
                self.fields["vuln_type"].queryset = VulnerabilityType.objects.filter(
                    category=self.instance.category
                )
            else:
                self.fields["vuln_type"].queryset = VulnerabilityType.objects.all()


class GlobalVulnerabilityForm(forms.ModelForm):
    class Meta:
        model = Vulnerability
        fields = "__all__"

        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "category": forms.Select(attrs={"class": "form-select"}),
            "vuln_type": forms.Select(attrs={"class": "form-select"}),
            # 🔁 Campos con TinyMCE
            "description": TinyMCE(attrs={"cols": 80, "rows": 20}),
            "remediation": TinyMCE(attrs={"cols": 80, "rows": 20}),
            "references": TinyMCE(attrs={"cols": 80, "rows": 20}),
            "cvss_31_vector": forms.TextInput(attrs={"class": "form-control"}),
            "cvss_31_score": forms.NumberInput(
                attrs={"class": "form-control", "step": "0.1", "min": "0", "max": "10"}
            ),
            "cvss_31_severity": forms.TextInput(
                attrs={"class": "form-control", "readonly": "readonly"}
            ),
            "cvss_40_vector": forms.TextInput(attrs={"class": "form-control"}),
            "cvss_40_score": forms.NumberInput(
                attrs={"class": "form-control", "step": "0.1", "min": "0", "max": "10"}
            ),
            "cvss_40_severity": forms.TextInput(
                attrs={"class": "form-control", "readonly": "readonly"}
            ),
            "remediation_complexity": forms.Select(attrs={"class": "form-select"}),
            "remediation_priority": forms.Select(attrs={"class": "form-select"}),
            "impact": forms.Select(attrs={"class": "form-select"}),
            "likelihood": forms.Select(attrs={"class": "form-select"}),
            "risk_rating": forms.TextInput(
                attrs={"class": "form-control", "readonly": "readonly"}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["vuln_type"].queryset = VulnerabilityType.objects.none()

        if "category" in self.data:
            try:
                category_id = int(self.data.get("category"))
                self.fields["vuln_type"].queryset = VulnerabilityType.objects.filter(
                    category_id=category_id
                )
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            if self.instance.category:
                self.fields["vuln_type"].queryset = VulnerabilityType.objects.filter(
                    category=self.instance.category
                )
            else:
                self.fields["vuln_type"].queryset = VulnerabilityType.objects.all()
