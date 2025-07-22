from django.urls import path
from . import views

urlpatterns = [
    path("", views.vulnerability_list_view, name="vulnerability_list"),
    path(
        "create/global/", views.create_global_vulnerability, name="create_global_vuln"
    ),
    path(
        "<int:pk>/edit/", views.update_vulnerability_view, name="update_vulnerability"
    ),
    path(
        "<int:pk>/delete/", views.delete_vulnerability_view, name="delete_vulnerability"
    ),
    path("<int:pk>/", views.vulnerability_detail_view, name="vulnerability_detail"),
    path("upload/", views.upload_vulnerabilities_view, name="upload_vulnerabilities"),
    path("ajax/load-vuln-types/", views.load_vuln_types, name="ajax_load_vuln_types"),
    path(
        "create/project/",
        views.create_project_vulnerability,
        name="create_project_vuln",
    ),
]
