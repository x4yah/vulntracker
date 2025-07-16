from django import forms
from .models import Vulnerability, VulnerabilityCategory, VulnerabilityType


class VulnerabilityForm(forms.ModelForm):
    class Meta:
        model = Vulnerability
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["type"].queryset = VulnerabilityType.objects.none()

        if "category" in self.data:
            try:
                category_id = int(self.data.get("category"))
                self.fields["type"].queryset = VulnerabilityType.objects.filter(
                    category_id=category_id
                )
            except (ValueError, TypeError):
                pass
