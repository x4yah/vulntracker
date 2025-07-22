def generate_vuln_code(project, vuln_type):
    prefix = f"{project.code_name}-{vuln_type.lower()}"
    from vulnerabilities.models import ProjectVulnerability  # Import interno

    count = (
        ProjectVulnerability.objects.filter(
            project=project, vulnerability_type=vuln_type
        ).count()
        + 1
    )
    return f"{prefix}-{str(count).zfill(3)}"
