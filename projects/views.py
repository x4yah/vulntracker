from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Max
from .models import Project
from .forms import ProjectForm
from .utils import generate_code_name


@login_required
def projects_overview_view(request):
    # 🔍 Determinar si el usuario es cliente (puedes adaptar esto a tu sistema de roles real)
    role = request.user.role
    sidebar = f"components/sidebar_{role}.html"
    is_client = request.user.groups.filter(name="Clientes").exists()

    # 🔎 Filtrar proyectos si es cliente
    if is_client:
        projects = Project.objects.filter(client__user=request.user)
        template = "projects/project_cards.html"
    else:
        projects = Project.objects.all()
        template = "projects/project_list.html"

    return render(
        request,
        template,
        {"projects": projects, "is_client": is_client, "sidebar_template": sidebar},
    )


@login_required
def project_create_view(request):
    role = request.user.role
    sidebar = f"components/sidebar_{role}.html"

    if request.method == "POST":
        form = ProjectForm(request.POST)

        if form.is_valid():
            project = form.save(commit=False)

            # 🧠 Si no se envió un alias, lo generamos desde backend
            if not project.code_name:
                project.code_name = generate_code_name(capitalize=True)

            project.created_by = request.user  # opcional si usas auditoría
            project.save()
            form.save_m2m()

            return redirect("projects_overview")

    else:
        # ✅ En GET, generamos alias y lo pasamos como valor inicial
        alias = generate_code_name(capitalize=True)
        form = ProjectForm(initial={"code_name": alias})

    return render(
        request,
        "projects/project_new.html",
        {"form": form, "sidebar_template": sidebar},
    )

@login_required
def project_edit_view(request, pk):
    role = request.user.role
    sidebar = f"components/sidebar_{role}.html"
    project = Project.objects.get(pk=pk)
    if request.method == "POST":
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect("projects_detail", pk=project.pk)
    else:
        form = ProjectForm(instance=project)
    return render(request, "projects/project_edit.html", {"form": form, "project": project, "sidebar_template": sidebar})

@login_required
def project_delete_view(request, pk):
    role = request.user.role
    sidebar = f"components/sidebar_{role}.html"
    project = get_object_or_404(Project, pk=pk)

    if request.method == "POST":
        project.delete()
        messages.success(request, f"Proyecto '{project.name}' eliminado correctamente.")
        return redirect("projects_overview")

    return render(request, "projects/project_confirm_delete.html", {
        "project": project,
        "sidebar_template": sidebar
    })