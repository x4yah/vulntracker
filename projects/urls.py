from django.urls import path
from . import views

urlpatterns = [
    # base
    path("", views.projects_overview_view, name="projects_overview"),
    # path("follow-up/", views.project_followup_view, name="projects_followup"),
    # path("reports/", views.project_reports_view, name="projects_reports"),
    path("new/", views.project_create_view, name="projects_new"),
    # projects details
    # path("<int:pk>/", views.projects_detail_view, name="projects_detail"),
    path("<int:pk>/edit/", views.project_edit_view, name="projects_edit"),
    path("<int:pk>/delete/", views.project_delete_view, name="projects_delete"),
    # path("<int:pk>/followups/", views.project_followups_view, name="projects_followups"),
    # path("<int:pk>/followups/<int:followup_pk>/edit/",
    # path("<int:pk>/followups/new/", views.project_followup_create_view, name="projects_followup_new"),
    # project reports
    # path("<int:pk>/reports/", views.project_reports_view, name="projects_reports"),
    # path("<int:pk>/reports/new/", views.project_report_create_view, name="projects_report_new"),
    # path("<int:pk>/reports/<int:report_pk>/edit", views.project_report_detail_edit, name="projects_report_detail_edit"),
    # path("<int:pk>/reports/<int:report_pk>/delete", views.project_report_delete_view, name="projects_report_delete"),
    # project vulns
    # path("<int:pk>/vulnerabilities/", views.project_vulnerabilities_view, name="projects_vulnerabilities"),
    # path("<int:pk>/vulnerabilities/new/", views.project_vulnerability_create_view, name="projects_vulnerability_new"),
    # path("<int:pk>/vulnerabilities/<int:vuln_pk>/edit", views.project_vulnerability_detail_view, name="projects_vulnerability_detail"),
    # path("<int:pk>/vulnerabilities/<int:vuln_pk>/delete", views.project_vulnerability_delete_view, name="projects_vulnerability_delete"),
]
