from django.shortcuts import render, redirect, get_object_or_404
from .models import Client, Contact
from .forms import ClientForm, ContactForm


# CLIENTS
def client_list_view(request):
    clients = Client.objects.all()
    role = request.user.role
    sidebar = f"components/sidebar_{role}.html"
    return render(
        request,
        "customers/client_list.html",
        {"clients": clients, "sidebar_template": sidebar},
    )


def client_new(request):
    role = request.user.role
    sidebar = f"components/sidebar_{role}.html"
    form = ClientForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        return redirect("clients_list")
    return render(
        request,
        "customers/client_form.html",
        {"form": form, "sidebar_template": sidebar},
    )


def client_edit(request, pk):
    client = get_object_or_404(Client, pk=pk)
    role = request.user.role
    sidebar = f"components/sidebar_{role}.html"
    form = ClientForm(request.POST or None, request.FILES or None, instance=client)
    if form.is_valid():
        form.save()
        return redirect("clients_list")
    return render(
        request,
        "customers/client_form.html",
        {"form": form, "client": client, "sidebar_template": sidebar},
    )


def client_details(request, pk):
    client = get_object_or_404(Client, pk=pk)
    contacts = Contact.objects.filter(client=client)
    role = request.user.role
    sidebar = f"components/sidebar_{role}.html"
    return render(
        request,
        "customers/client_details.html",
        {"client": client, "contacts": contacts, "sidebar_template": sidebar},
    )


def client_delete(request, pk):
    client = get_object_or_404(Client, pk=pk)
    client.delete()
    return redirect("clients_list")


def client_contacts(request, pk):
    client = get_object_or_404(Client, pk=pk)
    contacts = client.contacts.all()
    role = request.user.role
    sidebar = f"components/sidebar_{role}.html"
    return render(
        request,
        "customers/client_contacts.html",
        {"client": client, "contacts": contacts, "sidebar_template": sidebar},
    )


# 📁 Proyectos del cliente (por ahora como placeholder)
def client_projects(request, pk):
    client = get_object_or_404(Client, pk=pk)
    return render(request, "customers/client_projects.html", {"client": client})


# 🛡️ Vulnerabilidades por cliente
def client_vulnerabilities(request, pk):
    client = get_object_or_404(Client, pk=pk)
    return render(request, "customers/client_vulns.html", {"client": client})


# 📄 Reportes del cliente
def client_reports(request, pk):
    client = get_object_or_404(Client, pk=pk)
    return render(request, "customers/client_reports.html", {"client": client})


# 📆 Vista principal de seguimiento
def client_followup(request, pk):
    client = get_object_or_404(Client, pk=pk)
    return render(request, "customers/client_followup.html", {"client": client})


# ➕ Crear nuevo seguimiento
def client_followup_new(request, pk):
    client = get_object_or_404(Client, pk=pk)
    return render(request, "customers/client_followup_form.html", {"client": client})


# ✏️ Editar seguimiento existente
def client_followup_edit(request, pk, followup_pk):
    client = get_object_or_404(Client, pk=pk)
    return render(
        request,
        "customers/client_followup_form.html",
        {"client": client, "followup_pk": followup_pk},
    )


# 🗑️ Eliminar seguimiento
def client_followup_delete(request, pk, followup_pk):
    client = get_object_or_404(Client, pk=pk)
    # lógica para eliminar iría aquí
    return redirect("client_followup", pk=pk)


# CONTACTS
def contact_list_view(request):
    contacts = Contact.objects.select_related("client")
    role = request.user.role
    sidebar = f"components/sidebar_{role}.html"
    return render(
        request,
        "customers/contact_list.html",
        {"contacts": contacts, "sidebar_template": sidebar},
    )


def contact_new(request):
    form = ContactForm(request.POST or None)
    role = request.user.role
    sidebar = f"components/sidebar_{role}.html"
    if form.is_valid():
        form.save()
        return redirect("contacts_list")
    return render(
        request,
        "customers/contact_form.html",
        {"form": form, "sidebar_template": sidebar},
    )


def contact_detail(request, pk):
    contact = get_object_or_404(Contact, pk=pk)
    role = request.user.role
    sidebar = f"components/sidebar_{role}.html"
    return render(
        request,
        "customers/contact_detail.html",
        {"contact": contact, "sidebar_template": sidebar},
    )


def contact_edit(request, pk):
    contact = get_object_or_404(Contact, pk=pk)
    form = ContactForm(request.POST or None, instance=contact)
    role = request.user.role
    sidebar = f"components/sidebar_{role}.html"
    if form.is_valid():
        form.save()
        return redirect("contacts_list")
    return render(
        request,
        "customers/contact_form.html",
        {"form": form, "contact": contact, "sidebar_template": sidebar},
    )


def contact_delete(request, pk):
    contact = get_object_or_404(Contact, pk=pk)
    contact.delete()
    return redirect("contacts_list")
