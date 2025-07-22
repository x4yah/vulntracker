from django.urls import path
from . import views

urlpatterns = [
    path("clients/", views.client_list_view, name="clients_list"),
    path("clients/new", views.client_new, name="clients_new"),
    path("clients/<int:pk>", views.client_details, name="clients_details"),
    path("clients/<int:pk>/edit", views.client_edit, name="clients_edit"),
    path("clients/<int:pk>/delete", views.client_delete, name="clients_delete"),
    path("clients/<int:pk>/contacts", views.client_contacts, name="clients_contacts"),
    path("clients/<int:pk>/projects", views.client_projects, name="clients_projects"),
    path(
        "clients/<int:pk>/vulnerabilities",
        views.client_vulnerabilities,
        name="clients_vulnerabilities",
    ),
    path("clients/<int:pk>/reports", views.client_reports, name="clients_reports"),
    path("clients/<int:pk>/followup", views.client_followup, name="clients_followup"),
    path(
        "clients/<int:pk>/followup/new",
        views.client_followup_new,
        name="clients_followup_new",
    ),
    path(
        "clients/<int:pk>/followup/<int:followup_pk>/edit",
        views.client_followup_edit,
        name="clients_followup_edit",
    ),
    path(
        "clients/<int:pk>/followup/<int:followup_pk>/delete",
        views.client_followup_delete,
        name="clients_followup_delete",
    ),
    path("contacts/", views.contact_list_view, name="contacts_list"),
    path("contacts/new", views.contact_new, name="contacts_new"),
    path("contacts/<int:pk>/", views.contact_detail, name="contacts_detail"),
    path("contacts/<int:pk>/edit", views.contact_edit, name="contacts_edit"),
    path("contacts/<int:pk>/delete", views.contact_delete, name="contacts_delete"),
]
