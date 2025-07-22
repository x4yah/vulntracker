from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Vulnerability, VulnerabilityCategory, VulnerabilityType
from .forms import GlobalVulnerabilityForm, ProjectVulnerabilityForm
from django.contrib import messages
from django.http import JsonResponse
from django.core.exceptions import ValidationError

import yaml


@login_required
def create_global_vulnerability(request):
    form = GlobalVulnerabilityForm(request.POST or None)
    role = request.user.role
    sidebar = f"components/sidebar_{role}.html"
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("vulnerability_list")  # Ajusta al nombre de tu vista/listado
    return render(
        request,
        "vulnerabilities/global_vuln_form.html",
        {"form": form, "sidebar_template": sidebar},
    )


@login_required
def create_project_vulnerability(request):
    form = ProjectVulnerabilityForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect(
            "vulnerabilities:list_project"
        )  # Ajusta al nombre de tu vista/listado
    return render(request, "vulnerabilities/project_vuln_form.html", {"form": form})


@login_required
def update_vulnerability_view(request, pk):
    vuln = get_object_or_404(Vulnerability, pk=pk)
    form = GlobalVulnerabilityForm(
        request.POST or None, request.FILES or None, instance=vuln
    )
    role = request.user.role
    sidebar = f"components/sidebar_{role}.html"
    if form.is_valid():
        form.save()
        messages.success(request, "Vulnerabilidad actualizada.")
        return redirect("vulnerability_detail", pk=vuln.pk)
    return render(
        request,
        "vulnerabilities/global_vuln_form.html",
        {"form": form, "sidebar_template": sidebar},
    )


@login_required
def delete_vulnerability_view(request, pk):
    vuln = get_object_or_404(Vulnerability, pk=pk)
    role = request.user.role
    sidebar = f"components/sidebar_{role}.html"
    if request.method == "POST":
        vuln.delete()
        messages.success(request, "Vulnerabilidad eliminada.")
        return redirect("vulnerability_list")
    return render(
        request,
        "vulnerabilities/vuln_confirm_delete.html",
        {"vulnerability": vuln, "sidebar_template": sidebar},
    )


@login_required
def vulnerability_detail_view(request, pk):
    vuln = get_object_or_404(Vulnerability, pk=pk)
    role = request.user.role
    sidebar = f"components/sidebar_{role}.html"
    return render(
        request,
        "vulnerabilities/vuln_detail.html",
        {"vulnerability": vuln, "sidebar_template": sidebar},
    )


@login_required
def vulnerability_list_view(request):
    vulnerabilities = Vulnerability.objects.all()
    role = request.user.role
    sidebar = f"components/sidebar_{role}.html"
    return render(
        request,
        "vulnerabilities/vuln_list.html",
        {"vulnerabilities": vulnerabilities, "sidebar_template": sidebar},
    )


@login_required
def upload_vulnerabilities_view(request):
    role = request.user.role
    sidebar = f"components/sidebar_{role}.html"
    if request.method == "POST":
        yaml_file = request.FILES.get("yaml_file")
        if yaml_file:
            try:
                data = yaml.safe_load(yaml_file)
                entries = (
                    data if isinstance(data, list) else data.get("vulnerabilities", [])
                )
                for entry in entries:
                    vuln = Vulnerability(
                        title=entry.get("title", "Sin título"),
                        description=entry.get("description", ""),
                        remediation=entry.get("remediation", ""),
                        remediation_complexity=entry.get(
                            "remediation_complexity", "medium"
                        ),
                        remediation_priority=entry.get(
                            "remediation_priority", "medium"
                        ),
                        impact=entry.get("impact", "medium"),
                        likelihood=entry.get("likelihood", "medium"),
                        risk_rating="",
                        status=entry.get("status", "open"),
                    )
                    vuln.save()
                messages.success(request, "Vulnerabilidades cargadas correctamente.")
                return redirect("vulnerability_list")
            except yaml.YAMLError as e:
                messages.error(request, f"Error al parsear el YAML: {e}")
        else:
            messages.error(request, "No se envió ningún archivo.")
    return render(
        request, "vulnerabilities/vuln_upload.html", {"sidebar_template": sidebar}
    )


def load_vuln_types(request):
    category_id = request.GET.get("category")
    types = VulnerabilityType.objects.filter(category_id=category_id).values(
        "id", "name", "code"
    )
    return JsonResponse(list(types), safe=False)
