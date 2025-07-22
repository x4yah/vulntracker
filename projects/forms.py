from django import forms
from tinymce.widgets import TinyMCE
from django_select2.forms import Select2Widget, Select2MultipleWidget
from .models import Project
from customers.models import Client
from core.models import User, Role
#from core.models import Specialist  # Ajusta según tu modelo real
from .utils import generate_code_name

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = "__all__"
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "code_name": forms.TextInput(attrs={"class": "form-control"}),
            "client": Select2Widget(attrs={"class": "form-select"}),
            "leader": Select2Widget(attrs={"class": "form-select"}),
            "specialist": Select2MultipleWidget(attrs={"class": "form-select", "data-placeholder": "Selecciona especialistas"}),
            "start_date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "end_date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "status": forms.Select(attrs={"class": "form-select"}),
            "scope": TinyMCE(attrs={"cols": 80, "rows": 12}),
            "description":TinyMCE(attrs={"cols": 80, "rows": 12}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 🧠 Alias técnico sugerido si no se proporciona
        if not self.initial.get("code_name") and not self.data.get("code_name"):
            self.fields["code_name"].widget.attrs["placeholder"] = generate_code_name(capitalize=True)
            alias = generate_code_name(capitalize=True)
            self.initial["code_name"] = alias
            self.fields["code_name"].initial = alias  

        # 📡 Refuerzo visual si no aplica Select2Widget dinámico
        self.fields["client"].widget.attrs.update({"data-placeholder": "Selecciona un cliente"})
        self.fields["specialist"].widget.attrs.update({"data-placeholder": "Asignar especialista"})
        admin_role = Role.objects.get(name="Administrador")
        specialist_role = Role.objects.get(name="Especialista")
        allowed_users = User.objects.filter(role__in=[admin_role.id, specialist_role.id])
        self.fields["leader"].queryset = allowed_users
        self.fields["specialist"].queryset = allowed_users
        

        # ✅ Asegura queryset operativo (ajústalo si filtras por activos)
        self.fields["client"].queryset = Client.objects.all()
        #self.fields["specialist"].queryset = Specialist.objects.all()
